#!/usr/bin/env python3
"""
Test the specific Ball - Aluminum Cans - Fairfield, CA scenario 
to verify emission factor display is working correctly.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5002"
API_ENDPOINT = f"{BASE_URL}/api/compute_ghg_emissions"


def test_ball_fairfield_display():
    """
    Test the exact scenario reported by the user.
    """

    print("🧪 Testing Ball - Aluminum Cans - Fairfield, CA Display")
    print("=" * 60)

    # Exact scenario from user report
    test_payload = {
        "supplier_data": {
            "Supplier_and_Container": "Ball - Aluminum Cans - Fairfield, CA",
            "Container_Weight": 500.0,  # Example weight
            "Number_Of_Containers": 20   # Example count
        },
        "activity_rows": [
            {
                "Source_Description": "Test transportation",
                "Region": "UK",
                "Mode_of_Transport": "Road",
                "Scope": "Scope 3",
                "Type_Of_Activity_Data": "Distance",
                "Vehicle_Type": "Medium Duty Truck",
                "Distance_Travelled": 100.0,
                "Total_Weight_Of_Freight_InTonne": 10.0,
                "Units_of_Measurement": "km"
            }
        ]
    }

    print(f"📋 Test Scenario:")
    print(
        f"   Supplier: {test_payload['supplier_data']['Supplier_and_Container']}")
    print(
        f"   Container Weight: {test_payload['supplier_data']['Container_Weight']} kg")
    print(
        f"   Number of Containers: {test_payload['supplier_data']['Number_Of_Containers']}")

    try:
        # Send API request
        response = requests.post(
            API_ENDPOINT,
            json=test_payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code != 200:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False

        result = response.json()

        # Extract all relevant data
        manufacturing_details = result.get('manufacturing_details', {})
        supplier_emission_factor = manufacturing_details.get(
            'supplier_emission_factor')
        emission_factor_source = manufacturing_details.get(
            'emission_factor_source')
        manufacturing_emissions = result.get('manufacturing_emissions', 0)

        print(f"\n📊 API Response Analysis:")
        print(f"   Status: {result.get('status')}")
        print(f"   Supplier Emission Factor: {supplier_emission_factor}")
        print(f"   Emission Factor Source: {emission_factor_source}")
        print(
            f"   Manufacturing Emissions: {manufacturing_emissions:.3f} tonnes")

        # Verify the emission factor is correct
        expected_factor = 14.4
        if abs(supplier_emission_factor - expected_factor) < 0.001:
            print(
                f"✅ Backend emission factor is correct: {supplier_emission_factor}")
        else:
            print(
                f"❌ Backend emission factor incorrect: got {supplier_emission_factor}, expected {expected_factor}")
            return False

        # Simulate sessionStorage data that EmissionSummary.js would receive
        print(f"\n💾 Simulating EmissionSummary.js Data Structure:")

        # This is what would be stored in sessionStorage and loaded by EmissionSummary
        session_supplier_data = {
            "Supplier_and_Container": test_payload['supplier_data']['Supplier_and_Container'],
            "Container_Weight": test_payload['supplier_data']['Container_Weight'],
            "Number_Of_Containers": test_payload['supplier_data']['Number_Of_Containers']
            # Note: No Supplier_Emission_Factor - this is handled by backend now
        }

        session_emission_results = result

        print(f"   Session Supplier Data: {session_supplier_data}")
        print(
            f"   Has manufacturing_details: {'✅' if session_emission_results.get('manufacturing_details') else '❌'}")

        # Simulate the new EmissionSummary.js logic
        print(f"\n🔧 Simulating Updated EmissionSummary.js Logic:")

        # This matches the updated calculateTotals function
        emission_factor_for_display = 0

        if session_emission_results.get('manufacturing_details', {}).get('supplier_emission_factor'):
            emission_factor_for_display = float(
                session_emission_results['manufacturing_details']['supplier_emission_factor'])
            source = "API manufacturing_details"
        elif session_supplier_data.get('Supplier_Emission_Factor'):
            emission_factor_for_display = float(
                session_supplier_data['Supplier_Emission_Factor'])
            source = "Stored supplier data"
        else:
            emission_factor_for_display = 0
            source = "Default fallback"

        print(f"   Display Emission Factor: {emission_factor_for_display}")
        print(f"   Source: {source}")

        # Check if display would be correct
        if abs(emission_factor_for_display - expected_factor) < 0.001:
            print(
                f"✅ EmissionSummary display will show correct factor: {emission_factor_for_display}")
        else:
            print(
                f"❌ EmissionSummary display issue: would show {emission_factor_for_display}, expected {expected_factor}")
            return False

        # Calculate expected manufacturing emissions
        container_weight = test_payload['supplier_data']['Container_Weight']
        num_containers = test_payload['supplier_data']['Number_Of_Containers']
        expected_manufacturing = (
            container_weight * num_containers * expected_factor) / 1000

        print(f"\n🧮 Emissions Calculation Verification:")
        print(
            f"   Expected Manufacturing: {expected_manufacturing:.3f} tonnes")
        print(f"   API Manufacturing: {manufacturing_emissions:.3f} tonnes")

        if abs(manufacturing_emissions - expected_manufacturing) < 0.001:
            print(f"✅ Manufacturing emissions calculation correct")
        else:
            print(f"❌ Manufacturing emissions mismatch")
            return False

        print(f"\n🎉 All checks passed!")
        print(f"✅ Backend lookup working correctly (14.4 emission factor)")
        print(f"✅ API response includes manufacturing_details")
        print(f"✅ EmissionSummary.js will display correct factor")
        print(f"✅ Manufacturing emissions calculated correctly")

        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_ball_fairfield_display()

    if success:
        print(f"\n🚀 Issue Resolution Complete!")
        print(f"The Ball - Aluminum Cans - Fairfield, CA supplier should now display:")
        print(f"   • Supplier Emission Factor: 14.4 (not 0.00)")
        print(f"   • Correct manufacturing emissions calculation")
        print(f"   • Data sourced from Reference Matrix lookup")
    else:
        print(f"\n❌ Issues remain - further investigation needed")
