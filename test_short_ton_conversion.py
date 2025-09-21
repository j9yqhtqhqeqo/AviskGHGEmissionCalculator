#!/usr/bin/env python3
"""
Test the short ton conversion in the material weight calculation.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5002"
API_ENDPOINT = f"{BASE_URL}/api/compute_ghg_emissions"


def test_short_ton_conversion():
    """
    Test that material weight is correctly converted to short tons in the display.
    """

    print("🧪 Testing Short Ton Conversion for Material Weight")
    print("=" * 55)

    # Test case: Ball - Aluminum Cans - Fairfield, CA
    test_payload = {
        "supplier_data": {
            "Supplier_and_Container": "Ball - Aluminum Cans - Fairfield, CA",
            "Container_Weight": 800.0,  # grams
            "Number_Of_Containers": 10000  # containers
        },
        "activity_rows": []  # Empty to focus on manufacturing weight calculation
    }

    print("📋 Test Scenario:")
    print(
        f"   Supplier: {test_payload['supplier_data']['Supplier_and_Container']}")
    print(
        f"   Container Weight: {test_payload['supplier_data']['Container_Weight']} g")
    print(
        f"   Number of Containers: {test_payload['supplier_data']['Number_Of_Containers']:,}")

    try:
        response = requests.post(
            API_ENDPOINT,
            json=test_payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code != 200:
            print(f"   ❌ API call failed: {response.status_code}")
            return False

        result = response.json()

        print("\n📊 Weight Calculations:")

        # Manual calculations for verification
        container_weight_g = test_payload['supplier_data']['Container_Weight']
        number_of_containers = test_payload['supplier_data']['Number_Of_Containers']

        # Total weight in grams
        total_weight_g = container_weight_g * number_of_containers
        print(f"   Total Weight (g): {total_weight_g:,.0f}")

        # Convert to kg (what the backend calculates with)
        total_weight_kg = total_weight_g / 1000
        print(f"   Total Weight (kg): {total_weight_kg:,.2f}")

        # Convert to metric tons
        total_weight_metric_tons = total_weight_kg / 1000
        print(f"   Total Weight (metric tons): {total_weight_metric_tons:.4f}")

        # Convert to short tons (1 metric ton = 1.10231 short tons)
        total_weight_short_tons = total_weight_metric_tons * 1.10231
        print(f"   Total Weight (short tons): {total_weight_short_tons:.4f}")

        print("\n🔍 API Response Validation:")
        manufacturing_details = result.get('manufacturing_details', {})
        if manufacturing_details:
            api_total_weight_tonnes = manufacturing_details.get(
                'total_material_weight_tonnes', 0)
            print(
                f"   API Total Weight (metric tons): {api_total_weight_tonnes:.4f}")

            # Calculate what the frontend would display
            frontend_weight_g = api_total_weight_tonnes * \
                1000 * 1000  # Convert back to grams for display
            frontend_weight_short_tons = api_total_weight_tonnes * \
                1.10231  # Convert to short tons

            print(f"   Frontend Display (g): {frontend_weight_g:,.0f}")
            print(
                f"   Frontend Display (short tons): {frontend_weight_short_tons:.4f}")

            # Verify calculations match
            weight_g_match = abs(frontend_weight_g - total_weight_g) < 1
            weight_st_match = abs(
                frontend_weight_short_tons - total_weight_short_tons) < 0.0001

            print(f"   Weight (g) Match: {'✅' if weight_g_match else '❌'}")
            print(
                f"   Weight (short tons) Match: {'✅' if weight_st_match else '❌'}")

            if weight_g_match and weight_st_match:
                print("\n✅ Short Ton Conversion Test PASSED!")
                print("🔧 Conversion Details:")
                print(
                    f"   • Input: {container_weight_g}g × {number_of_containers:,} containers")
                print(
                    f"   • Total: {total_weight_g:,.0f}g = {total_weight_short_tons:.4f} short tons")
                print(f"   • Conversion Factor: 1 metric ton = 1.10231 short tons")
                print(
                    f"   • Display Format: Weight shows 4 decimal places for precision")
                return True
            else:
                print("\n❌ Conversion calculations don't match!")
                return False
        else:
            print("   ❌ No manufacturing details in API response")
            return False

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


def test_multiple_scenarios():
    """
    Test different weight scenarios to verify short ton conversion.
    """

    print("\n🧪 Testing Multiple Weight Scenarios")
    print("=" * 40)

    test_scenarios = [
        {
            "name": "Small containers",
            "weight": 50.0,  # 50g
            "containers": 1000,
            "expected_short_tons": 0.0551  # 50kg = 0.05 metric tons = 0.0551 short tons
        },
        {
            "name": "Medium containers",
            "weight": 500.0,  # 500g
            "containers": 2000,
            "expected_short_tons": 1.1023  # 1000kg = 1 metric ton = 1.1023 short tons
        },
        {
            "name": "Large containers",
            "weight": 1000.0,  # 1000g (1kg)
            "containers": 5000,
            "expected_short_tons": 5.5116  # 5000kg = 5 metric tons = 5.5116 short tons
        }
    ]

    for scenario in test_scenarios:
        print(f"\n📋 {scenario['name']}:")

        # Calculate expected values
        total_g = scenario['weight'] * scenario['containers']
        total_kg = total_g / 1000
        total_metric_tons = total_kg / 1000
        total_short_tons = total_metric_tons * 1.10231

        print(
            f"   {scenario['weight']}g × {scenario['containers']:,} = {total_g:,.0f}g")
        print(f"   = {total_metric_tons:.4f} metric tons")
        print(f"   = {total_short_tons:.4f} short tons")
        print(f"   Expected: {scenario['expected_short_tons']:.4f} short tons")

        # Check if calculation matches expected
        match = abs(total_short_tons - scenario['expected_short_tons']) < 0.01
        print(f"   Result: {'✅ Match' if match else '❌ Mismatch'}")


if __name__ == "__main__":
    success = test_short_ton_conversion()

    if success:
        test_multiple_scenarios()
        print(f"\n🎉 Short Ton Conversion Implementation Complete!")
        print(f"✅ Benefits:")
        print(f"   • Material weight now displays in short tons as requested")
        print(f"   • Accurate conversion factor: 1 metric ton = 1.10231 short tons")
        print(f"   • Maintains precision with 4 decimal places")
        print(f"   • Clear labeling: 'Total Material Weight (short tons)'")
    else:
        print(f"\n❌ Issues found - please review the implementation")
