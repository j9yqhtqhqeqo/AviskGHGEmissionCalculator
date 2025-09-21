#!/usr/bin/env python3
"""
CO2 Emissions Validation Script

This script validates the calculate_co2_emissions method against the test data
in Co2TestDataFreightDistance.csv by running individual test cases and comparing results.
"""

import sys
import os
import csv
import math

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
sys.path.insert(0, backend_path)

try:
    from Components.Supplier_Input import Supplier_Input
    from Components.reference_ef import Reference_EF_Freight_CO2, Reference_Unit_Conversion
    from Services.Co2FossilFuelCalculator import Co2FossilFuelCalculator
    from config import get_config
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def load_test_data():
    """Load test data from Co2TestDataFreightDistance.csv."""
    test_data_path = os.path.join(os.path.dirname(
        __file__), '..', 'Data', 'Co2TestDataFreightDistance.csv')
    test_cases = []

    try:
        with open(test_data_path, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                if row:
                    test_cases.append({
                        'source_description': row.get('Source Description', ''),
                        'region': row.get('Region', ''),
                        'mode_of_transport': row.get('Mode of Transport', ''),
                        'scope': row.get('Scope', ''),
                        'type_of_activity_data': row.get('Type of Activity Data', ''),
                        'vehicle_type': row.get('Vehicle Type', ''),
                        'distance_travelled': float(row.get('Distance Travelled', 0)),
                        'total_weight': float(row.get('Total Weight of Freight (tonne)', 0)),
                        'units_of_measurement': row.get('Units of Measurement (Tonne Miles)', ''),
                        'expected_co2': float(row.get('Fossil Fuel CO2\n(metric tonnes)', 0))
                    })

        print(f"✅ Loaded {len(test_cases)} test cases")
        return test_cases

    except FileNotFoundError:
        print(f"❌ Test data file not found: {test_data_path}")
        return []
    except Exception as e:
        print(f"❌ Error loading test data: {str(e)}")
        return []


def initialize_calculator():
    """Initialize the CO2 calculator with reference data."""
    try:
        config = get_config()

        # Initialize reference data
        ef_freight_csv_path = config.get_csv_path('ef_freight_co2')
        unit_conversion_csv_path = config.get_csv_path('unit_conversion')

        reference_ef_freight_co2 = Reference_EF_Freight_CO2(
            ef_freight_csv_path)
        reference_unit_conversion = Reference_Unit_Conversion(
            unit_conversion_csv_path)

        # Initialize CO2 calculator
        calculator = Co2FossilFuelCalculator(
            reference_ef_fuel_use_co2=None,
            reference_ef_freight_co2=reference_ef_freight_co2,
            reference_unit_conversion=reference_unit_conversion
        )

        print("✅ CO2 calculator initialized successfully")
        return calculator

    except Exception as e:
        print(f"❌ Error initializing calculator: {str(e)}")
        return None


def create_supplier_input(test_case):
    """Create a Supplier_Input object from test case data."""
    return Supplier_Input(
        Supplier_and_Container="Test Supplier",
        Container_Weight=0.0,
        Number_Of_Containers=1,
        Source_Description=test_case['source_description'],
        Region=test_case['region'],
        Mode_of_Transport=test_case['mode_of_transport'],
        Scope=test_case['scope'],
        Type_Of_Activity_Data=test_case['type_of_activity_data'],
        Vehicle_Type=test_case['vehicle_type'],
        Distance_Travelled=test_case['distance_travelled'],
        Total_Weight_Of_Freight_InTonne=test_case['total_weight'],
        Num_Of_Passenger=None,
        Units_of_Measurement=test_case['units_of_measurement'],
        Fuel_Used=None,
        Fuel_Amount=None,
        Unit_Of_Fuel_Amount=None
    )


def run_test_case(calculator, test_case, test_number):
    """Run a single test case and return the result."""
    print(f"\n--- Test {test_number}: {test_case['source_description']} ---")
    print(f"Vehicle: {test_case['vehicle_type']}")
    print(f"Region: {test_case['region']}")
    print(f"Distance: {test_case['distance_travelled']} km")
    print(f"Weight: {test_case['total_weight']} tonnes")
    print(f"Expected CO2: {test_case['expected_co2']} metric tonnes")

    try:
        # Create supplier input
        supplier_input = create_supplier_input(test_case)

        # Calculate CO2 emissions
        results = calculator.calculate_co2_emissions([supplier_input])

        if results and len(results) > 0:
            result = results[0]
            calculated_co2 = result['co2_emissions']
            emission_factor = result['emission_factor']
            status = result['status']

            print(f"Emission Factor: {emission_factor}")
            print(f"Calculated CO2: {calculated_co2} metric tonnes")
            print(f"Status: {status}")

            # Calculate relative error
            expected_co2 = test_case['expected_co2']
            if expected_co2 != 0:
                relative_error = abs(
                    (calculated_co2 - expected_co2) / expected_co2) * 100
                print(f"Relative Error: {relative_error:.2f}%")

                # Consider test passed if within 5% tolerance
                if relative_error <= 5.0:
                    print("✅ PASS - Within 5% tolerance")
                    return True, calculated_co2, emission_factor, relative_error
                else:
                    print("❌ FAIL - Outside 5% tolerance")
                    return False, calculated_co2, emission_factor, relative_error
            else:
                if abs(calculated_co2) < 0.001:
                    print("✅ PASS - Both values are effectively zero")
                    return True, calculated_co2, emission_factor, 0.0
                else:
                    print("❌ FAIL - Expected zero but got non-zero value")
                    return False, calculated_co2, emission_factor, float('inf')
        else:
            print("❌ FAIL - No results returned")
            return False, 0.0, 0.0, float('inf')

    except Exception as e:
        print(f"❌ FAIL - Exception: {str(e)}")
        return False, 0.0, 0.0, float('inf')


def generate_results_csv(results, output_path):
    """Generate a CSV file with detailed test results."""
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Test Number', 'Source Description', 'Vehicle Type', 'Region',
                'Distance (km)', 'Weight (tonnes)', 'Expected CO2', 'Calculated CO2',
                'Emission Factor', 'Relative Error (%)', 'Status'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for result in results:
                writer.writerow(result)

        print(f"📋 Results saved to: {output_path}")

    except Exception as e:
        print(f"❌ Error saving results: {str(e)}")


def main():
    """Main function to run all tests."""
    print("🧪 CO2 Emissions Calculator Validation")
    print("=" * 50)

    # Load test data
    test_cases = load_test_data()
    if not test_cases:
        print("❌ No test data available. Exiting.")
        return

    # Initialize calculator
    calculator = initialize_calculator()
    if not calculator:
        print("❌ Failed to initialize calculator. Exiting.")
        return

    # Run all test cases
    results = []
    passed_tests = 0
    failed_tests = 0

    for i, test_case in enumerate(test_cases, 1):
        success, calculated_co2, emission_factor, relative_error = run_test_case(
            calculator, test_case, i)

        if success:
            passed_tests += 1
        else:
            failed_tests += 1

        # Store result for CSV output
        results.append({
            'Test Number': i,
            'Source Description': test_case['source_description'],
            'Vehicle Type': test_case['vehicle_type'],
            'Region': test_case['region'],
            'Distance (km)': test_case['distance_travelled'],
            'Weight (tonnes)': test_case['total_weight'],
            'Expected CO2': test_case['expected_co2'],
            'Calculated CO2': calculated_co2,
            'Emission Factor': emission_factor,
            'Relative Error (%)': f"{relative_error:.2f}" if relative_error != float('inf') else "N/A",
            'Status': "PASS" if success else "FAIL"
        })

    # Generate summary
    total_tests = passed_tests + failed_tests
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Pass Rate: {pass_rate:.1f}%")

    # Save detailed results
    output_path = os.path.join(os.path.dirname(
        __file__), 'co2_validation_results.csv')
    generate_results_csv(results, output_path)

    print(f"{'='*50}")

    if failed_tests > 0:
        print("\n❌ Some tests failed. Check the detailed results for analysis.")
    else:
        print("\n✅ All tests passed successfully!")


if __name__ == '__main__':
    main()
