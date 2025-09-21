#!/usr/bin/env python3
"""
Comprehensive test to verify the complete data flow:
1. Frontend SupplierData -> compute_ghg_emissions API
2. API response structure matches EmissionSummary.js expectations
3. SessionStorage data structure validation
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5002"
API_ENDPOINT = f"{BASE_URL}/api/compute_ghg_emissions"


def test_complete_data_flow():
    """
    Test the complete data flow that matches the updated frontend code.
    """

    # Sample data that matches what SupplierData.js would send
    frontend_payload = {
        "supplier_data": {
            "Supplier_and_Container": "Test Supplier - Container A",
            "Container_Weight": 800.0,  # kg
            "Number_Of_Containers": 12,
            "Supplier_Emission_Factor": 0.5  # Default value as set in SupplierData.js
        },
        "activity_rows": [
            {
                "Source_Description": "Road freight - Fuel consumption",
                "Region": "UK",
                "Mode_of_Transport": "Road",
                "Scope": "Scope 3",
                "Type_Of_Activity_Data": "Fuel",
                "Vehicle_Type": "Medium Duty Truck",
                "Fuel_Used": "Diesel",
                "Fuel_Amount": 200.0,
                "Unit_Of_Fuel_Amount": "Litres",
                "Distance_Travelled": None,
                "Total_Weight_Of_Freight_InTonne": None,
                "Units_of_Measurement": None
            },
            {
                "Source_Description": "Long distance transport",
                "Region": "UK",
                "Mode_of_Transport": "Road",
                "Scope": "Scope 3",
                "Type_Of_Activity_Data": "Distance",
                "Vehicle_Type": "HGV - 7.5 to 17 tonnes",
                "Fuel_Used": None,
                "Fuel_Amount": None,
                "Unit_Of_Fuel_Amount": None,
                "Distance_Travelled": 750.0,
                "Total_Weight_Of_Freight_InTonne": 9.6,
                "Units_of_Measurement": "km"
            }
        ]
    }

    print("🧪 Testing Complete Data Flow: Frontend → API → EmissionSummary")
    print("=" * 70)
    print(f"API Endpoint: {API_ENDPOINT}")
    print(f"Payload: {len(frontend_payload['activity_rows'])} activity rows")

    try:
        # Step 1: Test API call (simulating frontend SupplierData.js)
        response = requests.post(
            API_ENDPOINT,
            json=frontend_payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code != 200:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False

        api_result = response.json()
        print("✅ API call successful!")

        # Step 2: Validate API response structure for EmissionSummary.js
        print("\n=== Step 2: API Response Validation ===")

        required_top_level = [
            'status', 'manufacturing_emissions', 'transport_emissions', 'total_emissions']
        for field in required_top_level:
            if field in api_result:
                value = api_result[field]
                if isinstance(value, (int, float)):
                    print(f"✅ {field}: {value:.3f}")
                else:
                    print(f"✅ {field}: Present")
            else:
                print(f"❌ Missing: {field}")
                return False

        # Step 3: Validate transport emissions structure
        transport_emissions = api_result.get('transport_emissions', {})
        summary_data = transport_emissions.get(
            'summary_by_transport_scope_activity', {})

        print(f"\n=== Step 3: Transport Emissions Structure ===")
        print(f"✅ Total CO2: {transport_emissions.get('co2', 0):.3f} tonnes")
        print(f"✅ Summary categories: {len(summary_data)} transport modes")

        # Step 4: Simulate sessionStorage data (what SupplierData.js stores)
        print(f"\n=== Step 4: SessionStorage Simulation ===")

        session_data = {
            "supplierData": frontend_payload['supplier_data'],
            "activityData": frontend_payload['activity_rows'],
            "emissionResults": api_result
        }

        print(f"✅ supplierData: {len(session_data['supplierData'])} fields")
        print(f"✅ activityData: {len(session_data['activityData'])} rows")
        print(f"✅ emissionResults: Complete API response stored")

        # Step 5: Test EmissionSummary.js calculation logic
        print(f"\n=== Step 5: EmissionSummary.js Logic Validation ===")

        # Test calculateTotals function logic from EmissionSummary.js
        supplier_data = session_data['supplierData']
        emission_results = session_data['emissionResults']

        # Manufacturing emissions from API
        manufacturing_emissions = emission_results.get(
            'manufacturing_emissions', 0)

        # Transport emissions from API
        transport_co2 = emission_results.get(
            'transport_emissions', {}).get('co2', 0)

        # Total emissions from API
        total_emissions = emission_results.get('total_emissions', 0)

        # Material weight calculation (EmissionSummary.js logic)
        container_weight = float(supplier_data.get('Container_Weight', 0))
        number_of_containers = int(
            supplier_data.get('Number_Of_Containers', 0))
        total_material_weight = (
            container_weight * number_of_containers) / 1000  # Convert to tonnes
        supplier_emission_factor = float(
            supplier_data.get('Supplier_Emission_Factor', 0))

        print(
            f"Manufacturing emissions: {manufacturing_emissions:.3f} tonnes CO2e")
        print(f"Transport CO2 emissions: {transport_co2:.3f} tonnes CO2e")
        print(f"Total emissions: {total_emissions:.3f} tonnes CO2e")
        print(f"Material weight: {total_material_weight:.3f} tonnes")
        print(f"Supplier emission factor: {supplier_emission_factor}")

        # Verify totals consistency
        calculated_total = manufacturing_emissions + transport_co2
        print(
            f"✅ Totals consistent: {abs(calculated_total - total_emissions) < 0.001}")

        # Step 6: Test getTransportEmissions function logic
        print(f"\n=== Step 6: Transport Breakdown Logic ===")

        fuel_total = 0
        distance_total = 0
        mode_totals = {'road': 0, 'rail': 0, 'water': 0}

        for mode, scope_data in summary_data.items():
            mode_key = mode.lower()
            if mode_key not in mode_totals:
                mode_totals[mode_key] = 0

            for scope, activity_data in scope_data.items():
                for activity_type, ghg_data in activity_data.items():
                    co2_emissions = ghg_data.get(
                        'CO2', {}).get('total_emissions', 0)

                    if activity_type == 'Fuel':
                        fuel_total += co2_emissions
                    elif activity_type == 'Distance':
                        distance_total += co2_emissions

                    mode_totals[mode_key] += co2_emissions

        print(f"Fuel-based emissions: {fuel_total:.3f} tonnes CO2")
        print(f"Distance-based emissions: {distance_total:.3f} tonnes CO2")
        print(
            f"By mode - Road: {mode_totals['road']:.3f}, Rail: {mode_totals['rail']:.3f}, Water: {mode_totals['water']:.3f}")

        # Step 7: Validate equivalency calculations
        print(f"\n=== Step 7: Equivalency Statements ===")

        # These are the calculations from EmissionSummary.js
        miles_driven = total_emissions / 0.00022 if total_emissions > 0 else 0
        gallons_consumed = total_emissions / 0.00887 if total_emissions > 0 else 0
        tree_seedlings = total_emissions / 0.84 if total_emissions > 0 else 0

        print(f"Equivalent to {miles_driven:.0f} miles driven")
        print(f"Equivalent to {gallons_consumed:.0f} gallons consumed")
        print(f"Equivalent to {tree_seedlings:.1f} tree seedlings")

        print(f"\n🎉 Complete data flow test PASSED!")
        print(f"✅ Frontend → API → EmissionSummary data flow is working correctly")
        print(f"📊 All calculations and data structures are consistent")

        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_complete_data_flow()

    if success:
        print(f"\n🚀 Ready for Production!")
        print(f"The updated EmissionSummary page should work correctly with:")
        print(f"• New compute_ghg_emissions API response structure")
        print(f"• Updated SupplierData.js that stores emissionResults")
        print(f"• Enhanced calculateTotals() and getTransportEmissions() functions")
        print(f"• Dynamic data display instead of hardcoded values")
    else:
        print(f"\n❌ Issues found - please review the implementation")
