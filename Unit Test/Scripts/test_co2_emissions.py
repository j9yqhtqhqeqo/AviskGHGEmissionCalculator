#!/usr/bin/env python3
"""
Unit Test Script for CO2 Emissions Calculator

This script tests the Co2FossilFuelCalculator.calculate_co2_emissions method
using the test data from Co2TestDataFreightDistance.csv to ensure calculated values match expected results.
"""

from Components.Supplier_Input import Supplier_Input
from Components.reference_ef import Reference_EF_Freight_CO2, Reference_Unit_Conversion
from Services.Co2FossilFuelCalculator import Co2FossilFuelCalculator
from config import get_config
import sys
import os
import csv
import math
from typing import List, Dict, Any

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
sys.path.insert(0, backend_path)

# Import required classes


class Co2EmissionsTestRunner:
    """Test runner for CO2 emissions calculations."""

    def __init__(self):
        """Initialize the test runner with reference data."""
        self.config = get_config()
        self.test_data_path = os.path.join(os.path.dirname(
            __file__), '..', 'Data', 'Co2TestDataFreightDistance.csv')

        # Initialize reference data
        ef_freight_csv_path = self.config.get_csv_path('ef_freight_co2')
        unit_conversion_csv_path = self.config.get_csv_path('unit_conversion')

        self.reference_ef_freight_co2 = Reference_EF_Freight_CO2(
            ef_freight_csv_path)
        self.reference_unit_conversion = Reference_Unit_Conversion(
            unit_conversion_csv_path)

        # Initialize CO2 calculator
        self.co2_calculator = Co2FossilFuelCalculator(
            reference_ef_fuel_use_co2=None,  # Not needed for this test
            reference_ef_freight_co2=self.reference_ef_freight_co2,
            reference_unit_conversion=self.reference_unit_conversion
        )

        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0

    def load_test_data(self) -> List[Dict[str, Any]]:
        """Load test data from Co2TestDataFreightDistance.csv file."""
        test_data = []

        try:
            with open(self.test_data_path, 'r', encoding='utf-8-sig') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    if row:  # Check if row is not empty
                        test_data.append({
                            'Source Description': row.get('Source Description', ''),
                            'Region': row.get('Region', ''),
                            'Mode of Transport': row.get('Mode of Transport', ''),
                            'Scope': row.get('Scope', ''),
                            'Type of Activity Data': row.get('Type of Activity Data', ''),
                            'Vehicle Type': row.get('Vehicle Type', ''),
                            'Distance Travelled': float(row.get('Distance Travelled', 0)),
                            'Total Weight of Freight (tonne)': float(row.get('Total Weight of Freight (tonne)', 0)),
                            'Units of Measurement (Tonne Miles)': row.get('Units of Measurement (Tonne Miles)', ''),
                            'Expected CO2 (metric tonnes)': float(row.get('Fossil Fuel CO2\n(metric tonnes)', 0))
                        })

            print(
                f"✅ Loaded {len(test_data)} test cases from Co2TestDataFreightDistance.csv")
            return test_data

        except FileNotFoundError:
            print(f"❌ Test data file not found: {self.test_data_path}")
            return []
        except Exception as e:
            print(f"❌ Error loading test data: {str(e)}")
            return []

    def create_supplier_input(self, test_case: Dict[str, Any]) -> Supplier_Input:
        """Create a Supplier_Input object from test case data."""
        return Supplier_Input(
            Supplier_and_Container="Test Supplier",
            Container_Weight=0.0,  # Not relevant for this test
            Number_Of_Containers=1,  # Not relevant for this test
            Source_Description=test_case['Source Description'],
            Region=test_case['Region'],
            Mode_of_Transport=test_case['Mode of Transport'],
            Scope=test_case['Scope'],
            Type_Of_Activity_Data=test_case['Type of Activity Data'],
            Vehicle_Type=test_case['Vehicle Type'],
            Distance_Travelled=test_case['Distance Travelled'],
            Total_Weight_Of_Freight_InTonne=test_case[
                'Total Weight of Freight (tonne)'],
            Num_Of_Passenger=None,
            Units_of_Measurement=test_case['Units of Measurement (Tonne Miles)'],
            Fuel_Used=None,  # Using distance/weight calculation, not fuel
            Fuel_Amount=None,
            Unit_Of_Fuel_Amount=None
        )

    def compare_results(self, calculated: float, expected: float, tolerance: float = 0.01) -> bool:
        """
        Compare calculated and expected results within a tolerance.

        Args:
            calculated: Calculated CO2 emissions value
            expected: Expected CO2 emissions value
            tolerance: Acceptable relative difference (default 1%)

        Returns:
            bool: True if values match within tolerance
        """
        if expected == 0:
            return abs(calculated) < 0.001  # Handle zero case

        relative_error = abs((calculated - expected) / expected)
        return relative_error <= tolerance

    def run_single_test(self, test_case: Dict[str, Any], test_number: int) -> Dict[str, Any]:
        """Run a single test case and return results."""
        print(
            f"\n--- Test Case {test_number}: {test_case['Source Description']} ---")
        print(f"Vehicle Type: {test_case['Vehicle Type']}")
        print(f"Region: {test_case['Region']}")
        print(f"Distance: {test_case['Distance Travelled']} km")
        print(f"Weight: {test_case['Total Weight of Freight (tonne)']} tonnes")
        print(
            f"Expected CO2: {test_case['Expected CO2 (metric tonnes)']} metric tonnes")

        # Create supplier input
        supplier_input = self.create_supplier_input(test_case)

        # Calculate CO2 emissions
        try:
            results = self.co2_calculator.calculate_co2_emissions(
                [supplier_input])

            if results and len(results) > 0:
                calculated_co2 = results[0]['co2_emissions']
                emission_factor = results[0]['emission_factor']
                status = results[0]['status']

                print(f"Emission Factor: {emission_factor}")
                print(f"Calculated CO2: {calculated_co2} metric tonnes")
                print(f"Status: {status}")

                # Compare results
                expected_co2 = test_case['Expected CO2 (metric tonnes)']
                is_match = self.compare_results(calculated_co2, expected_co2)

                if is_match:
                    print("✅ PASS - Values match within tolerance")
                    self.passed_tests += 1
                    result_status = "PASS"
                else:
                    relative_error = abs((calculated_co2 - expected_co2) /
                                         expected_co2) * 100 if expected_co2 != 0 else float('inf')
                    print(f"❌ FAIL - Relative error: {relative_error:.2f}%")
                    self.failed_tests += 1
                    result_status = "FAIL"

                return {
                    'test_number': test_number,
                    'source_description': test_case['Source Description'],
                    'vehicle_type': test_case['Vehicle Type'],
                    'region': test_case['Region'],
                    'expected_co2': expected_co2,
                    'calculated_co2': calculated_co2,
                    'emission_factor': emission_factor,
                    'status': result_status,
                    'error_message': None
                }
            else:
                print("❌ FAIL - No results returned")
                self.failed_tests += 1
                return {
                    'test_number': test_number,
                    'source_description': test_case['Source Description'],
                    'vehicle_type': test_case['Vehicle Type'],
                    'region': test_case['Region'],
                    'expected_co2': test_case['Expected CO2 (metric tonnes)'],
                    'calculated_co2': 0.0,
                    'emission_factor': 0.0,
                    'status': "FAIL",
                    'error_message': "No results returned"
                }

        except Exception as e:
            print(f"❌ FAIL - Exception occurred: {str(e)}")
            self.failed_tests += 1
            return {
                'test_number': test_number,
                'source_description': test_case['Source Description'],
                'vehicle_type': test_case['Vehicle Type'],
                'region': test_case['Region'],
                'expected_co2': test_case['Expected CO2 (metric tonnes)'],
                'calculated_co2': 0.0,
                'emission_factor': 0.0,
                'status': "FAIL",
                'error_message': str(e)
            }

    def run_all_tests(self) -> None:
        """Run all test cases and generate a summary report."""
        print("🧪 Starting CO2 Emissions Calculator Tests")
        print("=" * 60)

        # Load test data
        test_data = self.load_test_data()
        if not test_data:
            print("❌ No test data available. Exiting.")
            return

        # Run each test case
        for i, test_case in enumerate(test_data, 1):
            result = self.run_single_test(test_case, i)
            self.test_results.append(result)

        # Generate summary report
        self.generate_summary_report()

        # Generate detailed report
        self.generate_detailed_report()

    def generate_summary_report(self) -> None:
        """Generate and print a summary report."""
        total_tests = self.passed_tests + self.failed_tests
        pass_rate = (self.passed_tests / total_tests *
                     100) if total_tests > 0 else 0

        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY REPORT")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Pass Rate: {pass_rate:.1f}%")

        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(
                        f"  • Test {result['test_number']}: {result['source_description']}")
                    if result['error_message']:
                        print(f"    Error: {result['error_message']}")
                    else:
                        print(
                            f"    Expected: {result['expected_co2']}, Got: {result['calculated_co2']}")

        print("\n" + "=" * 60)

    def generate_detailed_report(self) -> None:
        """Generate a detailed CSV report."""
        report_path = os.path.join(os.path.dirname(
            __file__), 'co2_test_results.csv')

        try:
            with open(report_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'Test Number', 'Source Description', 'Vehicle Type', 'Region',
                    'Expected CO2', 'Calculated CO2', 'Emission Factor', 'Status', 'Error Message'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for result in self.test_results:
                    writer.writerow({
                        'Test Number': result['test_number'],
                        'Source Description': result['source_description'],
                        'Vehicle Type': result['vehicle_type'],
                        'Region': result['region'],
                        'Expected CO2': result['expected_co2'],
                        'Calculated CO2': result['calculated_co2'],
                        'Emission Factor': result['emission_factor'],
                        'Status': result['status'],
                        'Error Message': result['error_message'] or ''
                    })

            print(f"📋 Detailed report saved to: {report_path}")

        except Exception as e:
            print(f"❌ Error generating detailed report: {str(e)}")


def main():
    """Main function to run the CO2 emissions tests."""
    test_runner = Co2EmissionsTestRunner()
    test_runner.run_all_tests()


if __name__ == '__main__':
    main()
