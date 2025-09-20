#!/usr/bin/env python3
"""
Simple CO2 Emissions Test Script

Run this script to test the CO2 emissions calculations against the test data.
Usage: python run_co2_tests.py
"""

import subprocess
import sys
import os


def main():
    """Main function to execute the CO2 emissions test."""

    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the main test script
    test_script = os.path.join(script_dir, 'test_co2_emissions.py')

    print("🚀 Starting CO2 Emissions Calculator Tests...")
    print("=" * 60)

    try:
        # Execute the test script
        result = subprocess.run([sys.executable, test_script],
                                capture_output=False,
                                text=True,
                                cwd=script_dir)

        if result.returncode == 0:
            print("\n✅ Test execution completed successfully!")
        else:
            print(
                f"\n❌ Test execution failed with return code: {result.returncode}")

    except FileNotFoundError:
        print(f"❌ Test script not found: {test_script}")
    except Exception as e:
        print(f"❌ Error executing tests: {str(e)}")


if __name__ == '__main__':
    main()
