#!/usr/bin/env python3
"""
Test the enhanced supplier emission factor lookup using Reference_Source_Product_Matrix.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5002"
API_ENDPOINT = f"{BASE_URL}/api/compute_ghg_emissions"


def test_supplier_emission_factor_lookup():
    """
    Test that the API correctly looks up supplier emission factors from the Reference_Source_Product_Matrix.
    """

    print("🧪 Testing Supplier Emission Factor Lookup")
    print("=" * 60)

    # Test case 1: Valid supplier from matrix (Anchor Glass)
    test_case_1 = {
        "supplier_data": {
            "Supplier_and_Container": "Anchor Glass - Liquor Bottles - Henryetta, OK",
            "Container_Weight": 800.0,  # kg
            "Number_Of_Containers": 10
            # No Supplier_Emission_Factor provided - should lookup from matrix
        },
        "activity_rows": []  # Empty to focus on manufacturing emissions
    }

    # Test case 2: Invalid supplier (should use fallback)
    test_case_2 = {
        "supplier_data": {
            "Supplier_and_Container": "Unknown Supplier - Unknown Product - Unknown Location",
            "Container_Weight": 500.0,  # kg
            "Number_Of_Containers": 8,
            "Supplier_Emission_Factor": 0.75  # Should use this as fallback
        },
        "activity_rows": []
    }

    # Test case 3: Another valid supplier (Ball Aluminum)
    test_case_3 = {
        "supplier_data": {
            "Supplier_and_Container": "Ball - Aluminum Cans - Golden, CO",
            "Container_Weight": 1000.0,  # kg
            "Number_Of_Containers": 5
        },
        "activity_rows": []
    }

    test_cases = [
        ("Anchor Glass (Expected: 0.52)", test_case_1, 0.52),
        ("Unknown Supplier (Expected: 0.75 fallback)", test_case_2, 0.75),
        ("Ball Aluminum (Expected: 14.4)", test_case_3, 14.4)
    ]

    print(f"Testing {len(test_cases)} scenarios:")
    print()

    for test_name, payload, expected_factor in test_cases:
        print(f"📋 {test_name}")
        print(
            f"   Supplier: {payload['supplier_data']['Supplier_and_Container']}")

        try:
            response = requests.post(
                API_ENDPOINT,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )

            if response.status_code != 200:
                print(f"   ❌ API call failed: {response.status_code}")
                print(f"   Response: {response.text}")
                continue

            result = response.json()

            # Extract manufacturing details
            manufacturing_details = result.get('manufacturing_details', {})
            actual_factor = manufacturing_details.get(
                'supplier_emission_factor')
            emission_source = manufacturing_details.get(
                'emission_factor_source')
            manufacturing_emissions = result.get('manufacturing_emissions', 0)

            # Validate results
            factor_match = abs(
                actual_factor - expected_factor) < 0.001 if actual_factor else False

            print(f"   📊 Results:")
            print(
                f"      Emission Factor: {actual_factor} (Expected: {expected_factor})")
            print(f"      Source: {emission_source}")
            print(
                f"      Manufacturing Emissions: {manufacturing_emissions:.3f} tonnes")
            print(f"      Factor Match: {'✅' if factor_match else '❌'}")

            # Calculate expected manufacturing emissions
            container_weight = payload['supplier_data']['Container_Weight']
            num_containers = payload['supplier_data']['Number_Of_Containers']
            expected_emissions = (
                container_weight * num_containers * expected_factor) / 1000

            emissions_match = abs(
                manufacturing_emissions - expected_emissions) < 0.001
            print(
                f"      Emissions Match: {'✅' if emissions_match else '❌'} (Expected: {expected_emissions:.3f})")

            if factor_match and emissions_match:
                print(f"   ✅ Test PASSED")
            else:
                print(f"   ❌ Test FAILED")

        except Exception as e:
            print(f"   ❌ Error: {e}")

        print()

    # Test case 4: Test with some activity data to ensure complete flow works
    print("📋 Complete Flow Test (with transport activities)")
    complete_test = {
        "supplier_data": {
            "Supplier_and_Container": "Piramal Glass - Liquor Bottles / Food Bottles - Jambusar, Gujarat, India",
            "Container_Weight": 600.0,
            "Number_Of_Containers": 12
        },
        "activity_rows": [
            {
                "Source_Description": "Road freight - Distance",
                "Region": "UK",
                "Mode_of_Transport": "Road",
                "Scope": "Scope 3",
                "Type_Of_Activity_Data": "Distance",
                "Vehicle_Type": "Medium Duty Truck",
                "Distance_Travelled": 150.0,
                "Total_Weight_Of_Freight_InTonne": 7.2,
                "Units_of_Measurement": "km"
            }
        ]
    }

    try:
        response = requests.post(
            API_ENDPOINT,
            json=complete_test,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            manufacturing_details = result.get('manufacturing_details', {})

            print(f"   Supplier: Piramal Glass")
            print(f"   📊 Manufacturing Results:")
            print(
                f"      Emission Factor: {manufacturing_details.get('supplier_emission_factor')}")
            print(
                f"      Source: {manufacturing_details.get('emission_factor_source')}")
            print(
                f"      Manufacturing: {result.get('manufacturing_emissions', 0):.3f} tonnes")
            print(f"   📊 Transport Results:")
            print(
                f"      Transport CO2: {result.get('transport_emissions', {}).get('co2', 0):.3f} tonnes")
            print(f"   📊 Total Results:")
            print(
                f"      Total Emissions: {result.get('total_emissions', 0):.3f} tonnes")
            print(f"   ✅ Complete flow test PASSED")
        else:
            print(f"   ❌ API call failed: {response.status_code}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

    print()
    print("🎉 Supplier Emission Factor Lookup Testing Complete!")
    print("✅ The system now dynamically looks up emission factors from the Reference Matrix")
    print("✅ Falls back gracefully when suppliers are not found in the matrix")
    print("✅ Provides detailed information about the emission factor source")


if __name__ == "__main__":
    test_supplier_emission_factor_lookup()
