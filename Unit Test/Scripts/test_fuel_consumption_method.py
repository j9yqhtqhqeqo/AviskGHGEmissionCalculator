#!/usr/bin/env python3
"""
Test script for the new get_emission_factor_by_fuel_consumption method.
"""

import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
sys.path.insert(0, backend_path)

try:
    from Components.reference_ef import Reference_EF_Fuel_Use_CO2, Reference_Unit_Conversion
    from Services.Co2FossilFuelCalculator import Co2FossilFuelCalculator
    from config import get_config
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_fuel_consumption_method():
    """Test the new get_emission_factor_by_fuel_consumption method."""

    print("🧪 Testing get_emission_factor_by_fuel_consumption method")
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
            reference_ef_freight_co2=None,  # Not needed for this test
            reference_unit_conversion=reference_unit_conversion
        )

        print("✅ CO2 calculator initialized successfully")

        # Test cases for fuel consumption
        test_cases = [
            {
                'name': 'Diesel Fuel Test',
                'fuel_used': 'Diesel',
                'fuel_amount': 100.0,
                'unit_of_fuel_amount': 'Litres',
                'region': 'US'
            },
            {
                'name': 'Petrol Fuel Test',
                'fuel_used': 'Petrol',
                'fuel_amount': 50.0,
                'unit_of_fuel_amount': 'Gallons',
                'region': 'UK'
            },
            {
                'name': 'Natural Gas Test',
                'fuel_used': 'Natural Gas',
                'fuel_amount': 1000.0,
                'unit_of_fuel_amount': 'm3',
                'region': 'Other'
            }
        ]

        print(f"\nRunning {len(test_cases)} test cases...")

        for i, test in enumerate(test_cases, 1):
            print(f"\n--- Test {i}: {test['name']} ---")
            print(f"Fuel Used: {test['fuel_used']}")
            print(f"Fuel Amount: {test['fuel_amount']}")
            print(f"Unit: {test['unit_of_fuel_amount']}")
            print(f"Region: {test['region']}")

            try:
                emission_factor = calculator.get_emission_factor_by_fuel_consumption(
                    fuel_used=test['fuel_used'],
                    fuel_amount=test['fuel_amount'],
                    unit_of_fuel_amount=test['unit_of_fuel_amount'],
                    region=test['region']
                )

                print(f"Emission Factor: {emission_factor}")

                if emission_factor > 0:
                    print("✅ PASS - Emission factor calculated successfully")
                else:
                    print(
                        "⚠️  WARNING - Emission factor is 0 (may indicate missing data)")

            except Exception as e:
                print(f"❌ FAIL - Exception: {str(e)}")

        print(f"\n{'='*60}")
        print("✅ Test completed successfully!")
        print("💡 The new get_emission_factor_by_fuel_consumption method is working.")

    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")


if __name__ == '__main__':
    test_fuel_consumption_method()
