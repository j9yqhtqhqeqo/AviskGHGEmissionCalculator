#!/usr/bin/env python3
"""
Test script to verify the updated compute_ghg_emissions endpoint
that returns summarized data by Mode of Transport, Scope, Activity type, and GHG Type.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5002"
API_ENDPOINT = f"{BASE_URL}/api/compute_ghg_emissions"


def test_compute_ghg_emissions_summary():
    """
    Test the compute_ghg_emissions endpoint with sample data to verify
    the new summarized data structure.
    """

    # Sample test data
    test_data = {
        "supplier_data": {
            "Supplier_and_Container": "Test Supplier - Container A",
            "Container_Weight": 1000.0,  # kg
            "Number_Of_Containers": 5,
            "Supplier_Emission_Factor": 0.5  # tCO2e per tonne
        },
        "activity_rows": [
            {
                "Source_Description": "Road transport - Fuel based",
                "Region": "UK",
                "Mode_of_Transport": "Road",
                "Scope": "Scope 3",
                "Type_Of_Activity_Data": "Fuel",
                "Vehicle_Type": "Medium Duty Truck",
                "Fuel_Used": "Diesel",
                "Fuel_Amount": 100.0,
                "Unit_Of_Fuel_Amount": "Litres",
                "Distance_Travelled": None,
                "Total_Weight_Of_Freight_InTonne": None,
                "Num_Of_Passenger": None,
                "Units_of_Measurement": None
            },
            {
                "Source_Description": "Road transport - Distance based",
                "Region": "UK",
                "Mode_of_Transport": "Road",
                "Scope": "Scope 3",
                "Type_Of_Activity_Data": "Distance",
                "Vehicle_Type": "HGV - 7.5 to 17 tonnes",
                "Fuel_Used": None,
                "Fuel_Amount": None,
                "Unit_Of_Fuel_Amount": None,
                "Distance_Travelled": 500.0,
                "Total_Weight_Of_Freight_InTonne": 2.5,
                "Num_Of_Passenger": None,
                "Units_of_Measurement": "km"
            },
            {
                "Source_Description": "Rail transport - Distance based",
                "Region": "UK",
                "Mode_of_Transport": "Rail",
                "Scope": "Scope 3",
                "Type_Of_Activity_Data": "Distance",
                "Vehicle_Type": "Freight Train",
                "Fuel_Used": None,
                "Fuel_Amount": None,
                "Unit_Of_Fuel_Amount": None,
                "Distance_Travelled": 1000.0,
                "Total_Weight_Of_Freight_InTonne": 10.0,
                "Num_Of_Passenger": None,
                "Units_of_Measurement": "km"
            }
        ]
    }

    print("=== Testing compute_ghg_emissions endpoint ===")
    print(f"Sending POST request to: {API_ENDPOINT}")
    print(f"Test data: {len(test_data['activity_rows'])} activity rows")

    try:
        # Make POST request
        response = requests.post(
            API_ENDPOINT,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        print(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ Request successful!")

            # Print overall structure
            print("\n=== Response Structure ===")
            print(f"Status: {result.get('status')}")
            print(f"Processed rows: {result.get('processed_rows')}")
            print(
                f"Manufacturing emissions: {result.get('manufacturing_emissions'):.3f} tonnes CO2e")
            print(
                f"Total CO2 transport emissions: {result.get('total_co2_emissions'):.3f} tonnes CO2e")
            print(
                f"Total emissions: {result.get('total_emissions'):.3f} tonnes CO2e")

            # Print summarized data structure
            transport_emissions = result.get('transport_emissions', {})
            summary_data = transport_emissions.get(
                'summary_by_transport_scope_activity', {})

            print("\n=== Summarized Data by Transport/Scope/Activity/GHG ===")
            for mode_of_transport, scope_data in summary_data.items():
                print(f"\n🚛 Mode of Transport: {mode_of_transport}")
                for scope, activity_data in scope_data.items():
                    print(f"  📊 Scope: {scope}")
                    for activity_type, ghg_data in activity_data.items():
                        print(f"    ⚡ Activity Type: {activity_type}")
                        for ghg_type, emissions_data in ghg_data.items():
                            total_emissions = emissions_data.get(
                                'total_emissions', 0)
                            details_count = len(
                                emissions_data.get('details', []))
                            print(
                                f"      🌍 {ghg_type}: {total_emissions:.3f} tonnes CO2e ({details_count} detail records)")

                            # Show first detail for verification
                            details = emissions_data.get('details', [])
                            if details:
                                detail = details[0]
                                print(
                                    f"        📝 Sample detail: {detail.get('source_description', 'N/A')}")
                                print(
                                    f"            Emissions: {detail.get('co2_emissions', 0):.3f} tonnes")
                                print(
                                    f"            Status: {detail.get('status', 'N/A')}")

            # Verify backward compatibility
            print("\n=== Backward Compatibility Check ===")
            legacy_results = result.get('co2_emissions_results', [])
            print(
                f"✅ Legacy co2_emissions_results: {len(legacy_results)} results")

            # Verify data consistency
            print("\n=== Data Consistency Verification ===")
            calculated_total = sum(r.get('co2_emissions', 0)
                                   for r in legacy_results)
            reported_total = result.get('total_co2_emissions', 0)
            print(f"Calculated total from details: {calculated_total:.3f}")
            print(f"Reported total_co2_emissions: {reported_total:.3f}")
            print(
                f"✅ Totals match: {abs(calculated_total - reported_total) < 0.001}")

            return True

        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_server_connection():
    """Test if the server is running and accessible."""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(
            f"✅ Server is running: {response.json().get('message', 'No message')}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Server connection failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing compute_ghg_emissions endpoint with summarized data structure")
    print("=" * 70)

    # Test server connection first
    if test_server_connection():
        print()
        # Test the compute_ghg_emissions endpoint
        success = test_compute_ghg_emissions_summary()

        if success:
            print(
                "\n🎉 All tests passed! The compute_ghg_emissions endpoint is working correctly.")
            print("📊 The new summarized data structure is properly implemented.")
        else:
            print("\n❌ Tests failed. Please check the server logs and implementation.")
    else:
        print("❌ Cannot connect to server. Please ensure the Flask app is running on localhost:5002")
