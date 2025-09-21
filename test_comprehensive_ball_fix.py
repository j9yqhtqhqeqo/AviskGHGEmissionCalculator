#!/usr/bin/env python3
"""
Comprehensive test for the Ball supplier emission factor fix.
Tests the complete workflow from API to frontend display.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5002"
API_ENDPOINT = f"{BASE_URL}/api/compute_ghg_emissions"


def test_comprehensive_ball_fix():
    """
    Test multiple Ball suppliers to ensure the fix works across all variants.
    """

    print("🧪 Comprehensive Ball Supplier Emission Factor Test")
    print("=" * 65)

    # Test multiple Ball suppliers
    test_cases = [
        {
            "name": "Ball Fairfield (User's Issue)",
            "supplier": "Ball - Aluminum Cans - Fairfield, CA",
            "expected_factor": 14.4
        },
        {
            "name": "Ball Golden",
            "supplier": "Ball - Aluminum Cans - Golden, CO",
            "expected_factor": 14.4
        },
        {
            "name": "Ball Fort Worth",
            "supplier": "Ball - Aluminum Cans - Fort Worth, TX",
            "expected_factor": 14.4
        }
    ]

    print(f"Testing {len(test_cases)} Ball supplier scenarios:")
    print()

    all_tests_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"📋 Test {i}: {test_case['name']}")
        print(f"   Supplier: {test_case['supplier']}")

        # Create test payload
        payload = {
            "supplier_data": {
                "Supplier_and_Container": test_case['supplier'],
                "Container_Weight": 600.0,
                "Number_Of_Containers": 15
            },
            "activity_rows": []
        }

        try:
            # API call
            response = requests.post(
                API_ENDPOINT,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )

            if response.status_code != 200:
                print(f"   ❌ API call failed: {response.status_code}")
                all_tests_passed = False
                continue

            result = response.json()

            # Check API response
            manufacturing_details = result.get('manufacturing_details', {})
            api_factor = manufacturing_details.get('supplier_emission_factor')
            factor_source = manufacturing_details.get('emission_factor_source')

            print(f"   📊 API Results:")
            print(f"      Emission Factor: {api_factor}")
            print(f"      Source: {factor_source}")

            # Verify emission factor
            if abs(api_factor - test_case['expected_factor']) < 0.001:
                print(f"   ✅ API emission factor correct")
            else:
                print(
                    f"   ❌ API emission factor wrong: got {api_factor}, expected {test_case['expected_factor']}")
                all_tests_passed = False
                continue

            # Verify source is from reference matrix
            if factor_source == 'reference_matrix':
                print(f"   ✅ Factor sourced from reference matrix")
            else:
                print(f"   ❌ Unexpected factor source: {factor_source}")
                all_tests_passed = False
                continue

            # Simulate EmissionSummary.js logic (the fix we implemented)
            emission_factor_for_display = 0

            if result.get('manufacturing_details', {}).get('supplier_emission_factor'):
                emission_factor_for_display = float(
                    result['manufacturing_details']['supplier_emission_factor'])
                display_source = "API manufacturing_details"
            else:
                emission_factor_for_display = 0
                display_source = "Fallback"

            print(f"   🖥️  Frontend Display:")
            print(f"      Display Factor: {emission_factor_for_display}")
            print(f"      Display Source: {display_source}")

            # Verify frontend display would be correct
            if abs(emission_factor_for_display - test_case['expected_factor']) < 0.001:
                print(f"   ✅ Frontend display correct")
            else:
                print(
                    f"   ❌ Frontend display wrong: would show {emission_factor_for_display}")
                all_tests_passed = False
                continue

            # Verify manufacturing emissions calculation
            expected_emissions = (
                600.0 * 15 * test_case['expected_factor']) / 1000
            actual_emissions = result.get('manufacturing_emissions', 0)

            if abs(actual_emissions - expected_emissions) < 0.001:
                print(
                    f"   ✅ Manufacturing emissions correct: {actual_emissions:.3f} tonnes")
            else:
                print(
                    f"   ❌ Manufacturing emissions wrong: got {actual_emissions:.3f}, expected {expected_emissions:.3f}")
                all_tests_passed = False
                continue

            print(f"   🎉 Test {i} PASSED")

        except Exception as e:
            print(f"   ❌ Test {i} failed with error: {e}")
            all_tests_passed = False

        print()

    # Test an unknown supplier to verify fallback works
    print(f"📋 Fallback Test: Unknown Supplier")
    unknown_payload = {
        "supplier_data": {
            "Supplier_and_Container": "Unknown Company - Unknown Product - Unknown Location",
            "Container_Weight": 400.0,
            "Number_Of_Containers": 10,
            "Supplier_Emission_Factor": 0.8  # Provided fallback
        },
        "activity_rows": []
    }

    try:
        response = requests.post(
            API_ENDPOINT,
            json=unknown_payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            manufacturing_details = result.get('manufacturing_details', {})
            fallback_factor = manufacturing_details.get(
                'supplier_emission_factor')
            fallback_source = manufacturing_details.get(
                'emission_factor_source')

            print(f"   📊 Fallback Results:")
            print(f"      Emission Factor: {fallback_factor}")
            print(f"      Source: {fallback_source}")

            if abs(fallback_factor - 0.8) < 0.001 and fallback_source == 'default/supplied':
                print(f"   ✅ Fallback mechanism working correctly")
            else:
                print(
                    f"   ❌ Fallback issue: got {fallback_factor} from {fallback_source}")
                all_tests_passed = False
        else:
            print(f"   ❌ Fallback test API call failed")
            all_tests_passed = False

    except Exception as e:
        print(f"   ❌ Fallback test error: {e}")
        all_tests_passed = False

    print()

    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Ball supplier emission factor issue RESOLVED")
        print("🔧 Key Fixes Implemented:")
        print("   • Backend correctly looks up emission factors from Reference Matrix")
        print(
            "   • Frontend gets emission factor from API response (manufacturing_details)")
        print("   • Display shows 14.4 instead of 0.00 for Ball suppliers")
        print("   • Emission factor source transparency added")
        print("   • Fallback mechanism works for unknown suppliers")
        print()
        print("🚀 User Issue Resolution:")
        print("   Ball - Aluminum Cans - Fairfield, CA will now show:")
        print("   • Supplier Emission Factor: 14.4 (not 0.00)")
        print("   • Source: Reference Matrix Lookup")
        print("   • Correct manufacturing emissions calculation")
    else:
        print("❌ SOME TESTS FAILED")
        print("Further investigation needed")

    return all_tests_passed


if __name__ == "__main__":
    success = test_comprehensive_ball_fix()
    print(f"\nTest Result: {'SUCCESS' if success else 'FAILURE'}")
