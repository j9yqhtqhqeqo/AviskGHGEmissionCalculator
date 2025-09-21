#!/usr/bin/env python3
"""
Test script to verify that the CSV file name update is working correctly.
This script tests that the updated test files can properly load the renamed CSV file.
"""

import sys
import os
import csv

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
sys.path.insert(0, backend_path)


def test_csv_file_access():
    """Test that the CSV file can be accessed with the new name."""

    print("🧪 Testing CSV File Name Update")
    print("=" * 50)

    # Test the file path
    csv_file_path = os.path.join(os.path.dirname(
        __file__), '..', 'Data', 'Co2TestDataFreightDistance.csv')

    print(f"Looking for CSV file at: {csv_file_path}")

    # Check if file exists
    if os.path.exists(csv_file_path):
        print("✅ CSV file found successfully")

        # Try to read the file
        try:
            with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
                csv_reader = csv.DictReader(file)
                rows = list(csv_reader)

                print(f"✅ Successfully loaded {len(rows)} rows from CSV file")

                # Display first row to verify structure
                if rows:
                    print("\n📋 First row data:")
                    for key, value in rows[0].items():
                        print(f"  {key}: {value}")

                # Verify expected columns are present
                expected_columns = [
                    'Source Description',
                    'Region',
                    'Mode of Transport',
                    'Scope',
                    'Type of Activity Data',
                    'Vehicle Type',
                    'Distance Travelled',
                    'Total Weight of Freight (tonne)',
                    'Units of Measurement (Tonne Miles)',
                    'Fossil Fuel CO2\n(metric tonnes)'
                ]

                if rows:
                    actual_columns = list(rows[0].keys())
                    print(f"\n📊 CSV Structure Validation:")
                    print(f"Expected columns: {len(expected_columns)}")
                    print(f"Actual columns: {len(actual_columns)}")

                    missing_columns = []
                    for col in expected_columns:
                        if col not in actual_columns:
                            missing_columns.append(col)

                    if missing_columns:
                        print(f"⚠️  Missing columns: {missing_columns}")
                    else:
                        print("✅ All expected columns found")

                return True

        except Exception as e:
            print(f"❌ Error reading CSV file: {e}")
            return False
    else:
        print(f"❌ CSV file not found at {csv_file_path}")

        # List files in the Data directory
        data_dir = os.path.dirname(csv_file_path)
        if os.path.exists(data_dir):
            files = os.listdir(data_dir)
            print(f"Files in {data_dir}: {files}")

        return False


def test_updated_scripts():
    """Test that the updated test scripts reference the correct file."""

    print(f"\n🔧 Testing Updated Script References")
    print("=" * 50)

    test_files = [
        'test_co2_emissions.py',
        'validate_co2_emissions.py',
        'quick_test.py'
    ]

    for test_file in test_files:
        file_path = os.path.join(os.path.dirname(__file__), test_file)

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                if 'Co2TestDataFreightDistance.csv' in content:
                    print(
                        f"✅ {test_file}: Updated to use Co2TestDataFreightDistance.csv")
                elif 'Co2TestData.csv' in content:
                    print(
                        f"⚠️  {test_file}: Still references old Co2TestData.csv")
                else:
                    print(f"ℹ️  {test_file}: No direct CSV reference found")

            except Exception as e:
                print(f"❌ Error reading {test_file}: {e}")
        else:
            print(f"❌ {test_file}: File not found")


if __name__ == '__main__':
    print("🚀 CSV File Update Validation Test")
    print("=" * 60)

    # Test CSV file access
    csv_success = test_csv_file_access()

    # Test script updates
    test_updated_scripts()

    print(f"\n📋 Summary:")
    print(f"CSV File Access: {'✅ PASS' if csv_success else '❌ FAIL'}")

    if csv_success:
        print("🎉 CSV file name update successful!")
        print("All test scripts should now work with Co2TestDataFreightDistance.csv")
    else:
        print("⚠️  Please check the CSV file location and name")
