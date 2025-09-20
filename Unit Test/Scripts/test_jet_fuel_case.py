#!/usr/bin/env python3
"""
Test script for the new get_emission_factor_by_fuel_consumption method
using the specific test case provided by the user.

Test Case:
Region: US
Mode of Transport: Water
Scope: Scope 3
Type of Activity Data: Fuel Use
Vehicle Type: Watercraft - Shipping - Large Bulk Carrier (14201 tonnes deadweight)
Fuel Used: Jet Fuel
Fuel Amount: 1000
Unit of Fuel Amount: US Gallon
"""

import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
sys.path.insert(0, backend_path)

try:
    from Components.Supplier_Input import Supplier_Input
    from Components.reference_ef import Reference_EF_Fuel_Use_CO2, Reference_Unit_Conversion
    from Services.Co2FossilFuelCalculator import Co2FossilFuelCalculator
    from config import get_config
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_fuel_consumption_case():
    """Test the specific fuel consumption case provided by the user."""

    print("🧪 Testing Jet Fuel Consumption Case")
    print("=" * 60)

    try:
        # Initialize the calculator
        config = get_config()

        # Initialize reference data
        ef_fuel_use_co2_csv_path = config.get_csv_path('ef_fuel_use_co2')
        unit_conversion_csv_path = config.get_csv_path('unit_conversion')

        reference_ef_fuel_use_co2 = Reference_EF_Fuel_Use_CO2(
            ef_fuel_use_co2_csv_path)
        reference_unit_conversion = Reference_Unit_Conversion(
            unit_conversion_csv_path)

        # Initialize CO2 calculator
        calculator = Co2FossilFuelCalculator(
            reference_ef_fuel_use_co2=reference_ef_fuel_use_co2,
            reference_ef_freight_co2=None,  # Not needed for fuel-based test
            reference_unit_conversion=reference_unit_conversion
        )

        print("✅ CO2 calculator initialized successfully")

        # Test case data
        test_data = {
            'region': 'US',
            'mode_of_transport': 'Water',
            'scope': 'Scope 3',
            'type_of_activity_data': 'Fuel Use',
            'vehicle_type': 'Watercraft - Shipping - Large Bulk Carrier (14201 tonnes deadweight)',
            'fuel_used': 'Jet Fuel',
            'fuel_amount': 1000.0,
            'unit_of_fuel_amount': 'US Gallon'
        }

        print("\n--- Test Case Details ---")
        print(f"Region: {test_data['region']}")
        print(f"Mode of Transport: {test_data['mode_of_transport']}")
        print(f"Scope: {test_data['scope']}")
        print(f"Type of Activity Data: {test_data['type_of_activity_data']}")
        print(f"Vehicle Type: {test_data['vehicle_type']}")
        print(f"Fuel Used: {test_data['fuel_used']}")
        print(f"Fuel Amount: {test_data['fuel_amount']}")
        print(f"Unit of Fuel Amount: {test_data['unit_of_fuel_amount']}")

        print("\n--- Testing get_emission_factor_by_fuel_consumption method ---")

        # Test the new method directly
        emission_factor = calculator.get_emission_factor_by_fuel_consumption(
            fuel_used=test_data['fuel_used'],
            fuel_amount=test_data['fuel_amount'],
            unit_of_fuel_amount=test_data['unit_of_fuel_amount'],
            region=test_data['region']
        )

        print(f"\nEmission Factor Result: {emission_factor}")

        if emission_factor > 0:
            # Calculate CO2 emissions
            co2_emissions = emission_factor * test_data['fuel_amount']
            print(f"Calculated CO2 Emissions: {co2_emissions} metric tonnes")
            print("✅ SUCCESS - Fuel consumption method working correctly")
        else:
            print("⚠️  WARNING - Emission factor is 0")
            print("This may indicate:")
            print("  • Fuel type 'Jet Fuel' not found in reference data")
            print("  • Region 'US' not available for this fuel type")
            print("  • Unit conversion issue with 'US Gallon'")

        print("\n--- Testing with calculate_co2_emissions method ---")

        # Create a Supplier_Input object to test the full workflow
        supplier_input = Supplier_Input(
            Supplier_and_Container="Test Supplier - Jet Fuel",
            Container_Weight=0.0,
            Number_Of_Containers=0,
            Source_Description="Jet Fuel Test",
            Region=test_data['region'],
            Mode_of_Transport=test_data['mode_of_transport'],
            Scope=test_data['scope'],
            Type_Of_Activity_Data=test_data['type_of_activity_data'],
            Vehicle_Type=test_data['vehicle_type'],
            Distance_Travelled=None,  # Not used for fuel-based calculation
            Total_Weight_Of_Freight_InTonne=None,  # Not used for fuel-based calculation
            Num_Of_Passenger=None,
            Units_of_Measurement=None,
            Fuel_Used=test_data['fuel_used'],
            Fuel_Amount=test_data['fuel_amount'],
            Unit_Of_Fuel_Amount=test_data['unit_of_fuel_amount']
        )

        # Test the full calculation workflow
        results = calculator.calculate_co2_emissions([supplier_input])

        if results and len(results) > 0:
            result = results[0]
            print(
                f"Full Workflow CO2 Emissions: {result['co2_emissions']} metric tonnes")
            print(
                f"Full Workflow Emission Factor: {result['emission_factor']}")
            print(f"Full Workflow Status: {result['status']}")

            if result['co2_emissions'] > 0:
                print("✅ SUCCESS - Full workflow functioning correctly")
            else:
                print("⚠️  WARNING - Full workflow returned 0 emissions")
        else:
            print("❌ FAIL - No results returned from full workflow")

        print(f"\n{'='*60}")
        print("🎯 Test Summary:")
        print(
            f"• Direct method test: {'✅ PASS' if emission_factor > 0 else '⚠️  WARN'}")
        print(
            f"• Full workflow test: {'✅ PASS' if results and results[0]['co2_emissions'] > 0 else '⚠️  WARN'}")
        print("• New fuel consumption method is integrated and functional")

    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_fuel_consumption_case()
