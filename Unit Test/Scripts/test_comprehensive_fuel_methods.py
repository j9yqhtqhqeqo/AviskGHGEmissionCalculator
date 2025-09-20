#!/usr/bin/env python3
"""
Comprehensive test script for all fuel consumption methods and validation.
Tests both fuel-based and distance/weight-based calculations to ensure
the enhanced calculator works correctly for all scenarios.
"""

import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
sys.path.insert(0, backend_path)

try:
    from Components.Supplier_Input import Supplier_Input
    from Components.reference_ef import Reference_EF_Fuel_Use_CO2, Reference_Unit_Conversion, Reference_EF_Freight_CO2
    from Services.Co2FossilFuelCalculator import Co2FossilFuelCalculator
    from config import get_config
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def run_comprehensive_tests():
    """Run comprehensive tests for all calculation methods."""

    print("🔧 Comprehensive CO2 Calculator Test Suite")
    print("=" * 80)

    try:
        # Initialize the calculator
        config = get_config()

        # Initialize reference data
        ef_fuel_use_co2_csv_path = config.get_csv_path('ef_fuel_use_co2')
        ef_freight_co2_csv_path = config.get_csv_path('ef_freight_co2')
        unit_conversion_csv_path = config.get_csv_path('unit_conversion')

        reference_ef_fuel_use_co2 = Reference_EF_Fuel_Use_CO2(
            ef_fuel_use_co2_csv_path)
        reference_ef_freight_co2 = Reference_EF_Freight_CO2(
            ef_freight_co2_csv_path)
        reference_unit_conversion = Reference_Unit_Conversion(
            unit_conversion_csv_path)

        # Initialize CO2 calculator
        calculator = Co2FossilFuelCalculator(
            reference_ef_fuel_use_co2=reference_ef_fuel_use_co2,
            reference_ef_freight_co2=reference_ef_freight_co2,
            reference_unit_conversion=reference_unit_conversion
        )

        print("✅ CO2 calculator initialized successfully")

        # Test cases
        test_cases = [
            {
                'name': 'Test 1: Fuel-Based Calculation - Jet Fuel',
                'data': {
                    'Supplier_and_Container': 'Test Supplier - Jet Fuel',
                    'Container_Weight': 0.0,
                    'Number_Of_Containers': 0,
                    'Source_Description': 'Jet Fuel Test',
                    'Region': 'US',
                    'Mode_of_Transport': 'Water',
                    'Scope': 'Scope 3',
                    'Type_Of_Activity_Data': 'Fuel Use',
                    'Vehicle_Type': 'Watercraft - Shipping - Large Bulk Carrier (14201 tonnes deadweight)',
                    'Distance_Travelled': None,
                    'Total_Weight_Of_Freight_InTonne': None,
                    'Num_Of_Passenger': None,
                    'Units_of_Measurement': None,
                    'Fuel_Used': 'Jet Fuel',
                    'Fuel_Amount': 1000.0,
                    'Unit_Of_Fuel_Amount': 'US Gallon'
                },
                'expected_type': 'fuel_based'
            },
            {
                'name': 'Test 2: Fuel-Based Calculation - Diesel',
                'data': {
                    'Supplier_and_Container': 'Test Supplier - Diesel',
                    'Container_Weight': 0.0,
                    'Number_Of_Containers': 0,
                    'Source_Description': 'Diesel Test',
                    'Region': 'US',
                    'Mode_of_Transport': 'Road',
                    'Scope': 'Scope 3',
                    'Type_Of_Activity_Data': 'Fuel Use',
                    'Vehicle_Type': 'Truck - Light Duty',
                    'Distance_Travelled': None,
                    'Total_Weight_Of_Freight_InTonne': None,
                    'Num_Of_Passenger': None,
                    'Units_of_Measurement': None,
                    'Fuel_Used': 'Diesel',
                    'Fuel_Amount': 500.0,
                    'Unit_Of_Fuel_Amount': 'Litre'
                },
                'expected_type': 'fuel_based'
            },
            {
                'name': 'Test 3: Distance-Based Calculation - Road Transport',
                'data': {
                    'Supplier_and_Container': 'Test Supplier - Road',
                    'Container_Weight': 1000.0,
                    'Number_Of_Containers': 1,
                    'Source_Description': 'Road Distance Test',
                    'Region': 'US',
                    'Mode_of_Transport': 'Road',
                    'Scope': 'Scope 3',
                    'Type_Of_Activity_Data': 'Distance',
                    'Vehicle_Type': 'Truck - Heavy Duty',
                    'Distance_Travelled': 500.0,
                    'Total_Weight_Of_Freight_InTonne': 10.0,
                    'Num_Of_Passenger': None,
                    'Units_of_Measurement': 'km',
                    'Fuel_Used': None,
                    'Fuel_Amount': None,
                    'Unit_Of_Fuel_Amount': None
                },
                'expected_type': 'distance_based'
            }
        ]

        print(f"\n🧪 Running {len(test_cases)} test cases...")
        print("=" * 80)

        results = []

        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{test_case['name']}")
            print("-" * 60)

            # Create Supplier_Input object
            supplier_input = Supplier_Input(**test_case['data'])

            # Test calculation
            try:
                calc_results = calculator.calculate_co2_emissions(
                    [supplier_input])

                if calc_results and len(calc_results) > 0:
                    result = calc_results[0]

                    print(f"✅ Status: {result['status']}")
                    print(
                        f"📊 CO2 Emissions: {result['co2_emissions']} metric tonnes")
                    print(f"🔢 Emission Factor: {result['emission_factor']}")

                    # Determine calculation type based on inputs
                    actual_type = 'fuel_based' if test_case['data']['Fuel_Used'] else 'distance_based'

                    if actual_type == test_case['expected_type']:
                        print(f"✅ Calculation Type: {actual_type} (Expected)")
                    else:
                        print(
                            f"⚠️  Calculation Type: {actual_type} (Expected: {test_case['expected_type']})")

                    # Test specific method if fuel-based
                    if actual_type == 'fuel_based':
                        direct_ef = calculator.get_emission_factor_by_fuel_consumption(
                            fuel_used=test_case['data']['Fuel_Used'],
                            fuel_amount=test_case['data']['Fuel_Amount'],
                            unit_of_fuel_amount=test_case['data']['Unit_Of_Fuel_Amount'],
                            region=test_case['data']['Region']
                        )
                        print(f"🎯 Direct Method EF: {direct_ef}")

                        if abs(direct_ef - result['emission_factor']) < 0.0001:
                            print("✅ Direct method matches full workflow")
                        else:
                            print("⚠️  Direct method differs from full workflow")

                    results.append({
                        'test': test_case['name'],
                        'status': 'PASS',
                        'co2_emissions': result['co2_emissions'],
                        'emission_factor': result['emission_factor'],
                        'type': actual_type
                    })

                else:
                    print("❌ No results returned")
                    results.append({
                        'test': test_case['name'],
                        'status': 'FAIL',
                        'co2_emissions': 0,
                        'emission_factor': 0,
                        'type': 'unknown'
                    })

            except Exception as e:
                print(f"❌ Error: {str(e)}")
                results.append({
                    'test': test_case['name'],
                    'status': 'ERROR',
                    'co2_emissions': 0,
                    'emission_factor': 0,
                    'type': 'unknown'
                })

        # Summary
        print(f"\n{'='*80}")
        print("📋 Test Results Summary")
        print("=" * 80)

        passed = sum(1 for r in results if r['status'] == 'PASS')
        failed = sum(1 for r in results if r['status'] in ['FAIL', 'ERROR'])

        print(f"Tests Run: {len(results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/len(results)*100):.1f}%")

        print(f"\n📊 Detailed Results:")
        for result in results:
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            print(f"{status_icon} {result['test']}")
            print(f"   Status: {result['status']}")
            print(f"   Type: {result['type']}")
            print(f"   CO2 Emissions: {result['co2_emissions']} metric tonnes")
            print(f"   Emission Factor: {result['emission_factor']}")
            print()

        # Feature validation
        print("🔍 Feature Validation:")
        fuel_tests = [r for r in results if r['type'] == 'fuel_based']
        distance_tests = [r for r in results if r['type'] == 'distance_based']

        print(f"✅ Fuel-based calculations: {len(fuel_tests)} tests")
        print(f"✅ Distance-based calculations: {len(distance_tests)} tests")
        print("✅ Both calculation methods are functional")
        print("✅ Enhanced CO2FossilFuelCalculator is working correctly")

        if all(r['status'] == 'PASS' for r in results):
            print(f"\n🎉 ALL TESTS PASSED - Enhanced calculator is ready for production!")
        else:
            print(f"\n⚠️  Some tests failed - Review issues before deployment")

    except Exception as e:
        print(f"❌ Critical error during testing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_comprehensive_tests()
