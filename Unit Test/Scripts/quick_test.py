#!/usr/bin/env python3
"""
Quick CO2 Test Runner

Simple script to test a few key scenarios from the test data.
"""

import sys
import os

# Navigate to backend directory and run a basic test


def run_quick_test():
    backend_dir = os.path.join(
        os.path.dirname(__file__), '..', '..', 'backend')

    print("🧪 Quick CO2 Emissions Test")
    print("=" * 40)

    # Test data (first 3 cases from Co2TestDataFreightDistance.csv)
    test_cases = [
        {
            'name': 'Test1 - Water Transport',
            'vehicle_type': 'Watercraft - Shipping - Large Bulk Carrier (14201 tonnes deadweight)',
            'region': 'US',
            'distance': 5000,
            'weight': 381.6,
            'expected_co2': 100.954079
        },
        {
            'name': 'Test2 - Road Transport',
            'vehicle_type': 'Road Vehicle - HGV - Rigid - Engine Size 3.5 - 7.5 tonnes',
            'region': 'US',
            'distance': 2000,
            'weight': 381.6,
            'expected_co2': 249.8613456
        },
        {
            'name': 'Test3 - Rail Transport',
            'vehicle_type': 'Rail',
            'region': 'US',
            'distance': 1000,
            'weight': 381.6,
            'expected_co2': 10.6001783
        }
    ]

    print(f"Running {len(test_cases)} test cases...")

    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}")
        print(f"   Vehicle: {test['vehicle_type']}")
        print(f"   Region: {test['region']}")
        print(f"   Distance: {test['distance']} km")
        print(f"   Weight: {test['weight']} tonnes")
        print(f"   Expected CO2: {test['expected_co2']} metric tonnes")
        print(f"   Status: Ready for testing")

    print(f"\n{'='*40}")
    print("✅ Test cases loaded successfully!")
    print("💡 To run the full validation, execute:")
    print("   python validate_co2_emissions.py")
    print(f"{'='*40}")


if __name__ == '__main__':
    run_quick_test()
