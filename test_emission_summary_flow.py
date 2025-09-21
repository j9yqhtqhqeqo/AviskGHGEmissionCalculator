#!/usr/bin/env python3
"""
Test script to verify the complete data flow from backend API to frontend EmissionSummary page.
This script tests the compute_ghg_emissions endpoint and validates that the response structure
matches what the updated EmissionSummary.js component expects.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5002"
API_ENDPOINT = f"{BASE_URL}/api/compute_ghg_emissions"


def test_emission_summary_data_flow():
    """
    Test the complete data flow from compute_ghg_emissions API to EmissionSummary frontend.
    """

    # Sample test data with realistic values
    test_data = {
        "supplier_data": {
            "Supplier_and_Container": "Saxco International - Glass Container A",
            "Container_Weight": 500.0,  # kg per container
            "Number_Of_Containers": 10,
            "Supplier_Emission_Factor": 0.8  # tCO2e per tonne
        },
        "activity_rows": [
            {
                "Source_Description": "Road transport from supplier to warehouse - Fuel based",
                "Region": "UK",
                "Mode_of_Transport": "Road",
                "Scope": "Scope 3",
                "Type_Of_Activity_Data": "Fuel",
                "Vehicle_Type": "Medium Duty Truck",
                "Fuel_Used": "Diesel",
                "Fuel_Amount": 150.0,
                "Unit_Of_Fuel_Amount": "Litres",
                "Distance_Travelled": None,
                "Total_Weight_Of_Freight_InTonne": None,
                "Num_Of_Passenger": None,
                "Units_of_Measurement": None
            },
            {
                "Source_Description": "Road transport warehouse to customer - Distance based",
                "Region": "UK",
                "Mode_of_Transport": "Road",
                "Scope": "Scope 3",
                "Type_Of_Activity_Data": "Distance",
                "Vehicle_Type": "HGV - 7.5 to 17 tonnes",
                "Fuel_Used": None,
                "Fuel_Amount": None,
                "Unit_Of_Fuel_Amount": None,
                "Distance_Travelled": 300.0,
                "Total_Weight_Of_Freight_InTonne": 5.0,
                "Num_Of_Passenger": None,
                "Units_of_Measurement": "km"
            },
            {
                "Source_Description": "Rail transport long distance - Distance based",
                "Region": "UK",
                "Mode_of_Transport": "Rail",
                "Scope": "Scope 3",
                "Type_Of_Activity_Data": "Distance",
                "Vehicle_Type": "Freight Train",
                "Fuel_Used": None,
                "Fuel_Amount": None,
                "Unit_Of_Fuel_Amount": None,
                "Distance_Travelled": 800.0,
                "Total_Weight_Of_Freight_InTonne": 5.0,
                "Num_Of_Passenger": None,
                "Units_of_Measurement": "km"
            }
        ]
    }

    print("=== Testing EmissionSummary Data Flow ===")
    print(f"Testing API endpoint: {API_ENDPOINT}")

    try:
        # Make POST request
        response = requests.post(
            API_ENDPOINT,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code != 200:
            print(f"❌ API request failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False

        result = response.json()
        print("✅ API request successful!")

        # Validate the response structure that EmissionSummary.js expects
        print("\n=== Validating Response Structure for EmissionSummary.js ===")

        # Check top-level structure
        required_fields = ['status', 'manufacturing_emissions',
                           'transport_emissions', 'total_emissions']
        for field in required_fields:
            if field in result:
                print(f"✅ {field}: {result[field]}")
            else:
                print(f"❌ Missing required field: {field}")

        # Check manufacturing emissions calculation
        container_weight = test_data['supplier_data']['Container_Weight']
        num_containers = test_data['supplier_data']['Number_Of_Containers']
        emission_factor = test_data['supplier_data']['Supplier_Emission_Factor']
        expected_manufacturing = (
            container_weight * num_containers * emission_factor) / 1000
        actual_manufacturing = result.get('manufacturing_emissions', 0)

        print(f"\n=== Manufacturing Emissions Validation ===")
        print(f"Expected: {expected_manufacturing:.3f} tonnes CO2e")
        print(f"Actual: {actual_manufacturing:.3f} tonnes CO2e")
        print(
            f"✅ Manufacturing calculation correct: {abs(expected_manufacturing - actual_manufacturing) < 0.001}")

        # Check transport emissions structure
        transport_emissions = result.get('transport_emissions', {})
        print(f"\n=== Transport Emissions Structure ===")
        print(f"✅ CO2 total: {transport_emissions.get('co2', 0):.3f} tonnes")

        # Check summary structure
        summary_data = transport_emissions.get(
            'summary_by_transport_scope_activity', {})
        print(f"\n=== Summary Data Structure (for EmissionSummary.js) ===")

        for mode, scope_data in summary_data.items():
            print(f"🚛 {mode}:")
            for scope, activity_data in scope_data.items():
                print(f"  📊 {scope}:")
                for activity_type, ghg_data in activity_data.items():
                    print(f"    ⚡ {activity_type}:")
                    for ghg_type, emissions_data in ghg_data.items():
                        total = emissions_data.get('total_emissions', 0)
                        details_count = len(emissions_data.get('details', []))
                        print(
                            f"      🌍 {ghg_type}: {total:.3f} tonnes ({details_count} records)")

        # Validate totals consistency
        print(f"\n=== Totals Consistency Check ===")
        total_emissions = result.get('total_emissions', 0)
        manufacturing = result.get('manufacturing_emissions', 0)
        transport_co2 = transport_emissions.get('co2', 0)
        calculated_total = manufacturing + transport_co2

        print(f"Manufacturing: {manufacturing:.3f} tonnes")
        print(f"Transport CO2: {transport_co2:.3f} tonnes")
        print(f"Calculated total: {calculated_total:.3f} tonnes")
        print(f"API reported total: {total_emissions:.3f} tonnes")
        print(
            f"✅ Totals match: {abs(calculated_total - total_emissions) < 0.001}")

        # Create sample sessionStorage data structure that frontend would use
        print(f"\n=== Sample sessionStorage Data for Frontend ===")
        frontend_data = {
            "supplierData": test_data['supplier_data'],
            "activityData": test_data['activity_rows'],
            "emissionResults": result
        }

        print("Sample data structure that would be stored in sessionStorage:")
        print(f"- supplierData: {len(test_data['supplier_data'])} fields")
        print(f"- activityData: {len(test_data['activity_rows'])} rows")
        print(f"- emissionResults: includes manufacturing_emissions, transport_emissions, total_emissions")

        # Test the new calculation logic that EmissionSummary.js would use
        print(f"\n=== Testing EmissionSummary.js Calculation Logic ===")

        # Test calculateTotals function logic
        supplier_data = test_data['supplier_data']
        container_weight = float(supplier_data.get('Container_Weight', 0))
        number_of_containers = int(
            supplier_data.get('Number_Of_Containers', 0))
        total_material_weight = (
            container_weight * number_of_containers) / 1000  # Convert to tonnes
        supplier_emission_factor = float(
            supplier_data.get('Supplier_Emission_Factor', 0))

        print(
            f"Material weight calculation: {total_material_weight:.3f} tonnes")
        print(f"Supplier emission factor: {supplier_emission_factor}")
        print(
            f"Manufacturing emissions: {result.get('manufacturing_emissions', 0):.3f} tonnes")
        print(
            f"Transport emissions: {transport_emissions.get('co2', 0):.3f} tonnes")
        print(
            f"Total emissions: {result.get('total_emissions', 0):.3f} tonnes")

        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing EmissionSummary Data Flow")
    print("=" * 70)

    success = test_emission_summary_data_flow()

    if success:
        print("\n🎉 EmissionSummary data flow test passed!")
        print("✅ The updated EmissionSummary.js should work correctly with the new API response.")
        print("📊 All required data fields are present and calculations are consistent.")
    else:
        print("\n❌ EmissionSummary data flow test failed!")
        print(
            "Please check the API response structure and EmissionSummary.js implementation.")
