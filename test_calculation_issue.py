#!/usr/bin/env python3

# Test the calculation issue: 420.6415 * 14.4 should equal 6,057.2376, not 5495040.00

def test_basic_calculation():
    """Test the basic multiplication"""
    material_weight = 420.6415  # tonnes
    emission_factor = 14.4      # tCO2 per tonne

    expected_result = 6057.2376  # Manual calculation
    actual_result = material_weight * emission_factor

    print(f"Material Weight: {material_weight} tonnes")
    print(f"Emission Factor: {emission_factor} tCO2/tonne")
    print(f"Expected Result: {expected_result} tCO2")
    print(f"Actual Result: {actual_result} tCO2")
    print(f"Difference: {abs(actual_result - expected_result)}")

    return actual_result


def test_unit_conversion_scenarios():
    """Test various unit conversion scenarios that might cause the issue"""

    # Scenario 1: Container weight in grams, converted to tonnes incorrectly
    # grams (this would give 420.6415 kg, not tonnes)
    container_weight_g = 420641.5
    containers = 1

    # Incorrect conversion (dividing by 1000 instead of 1,000,000)
    wrong_tonnes = (container_weight_g * containers) / \
        1000  # This gives 420.6415 kg, not tonnes
    correct_tonnes = (container_weight_g * containers) / \
        1000000  # This gives 0.4206415 tonnes

    emission_factor = 14.4

    wrong_result = wrong_tonnes * emission_factor
    correct_result = correct_tonnes * emission_factor

    print("\n--- Unit Conversion Test ---")
    print(f"Container Weight: {container_weight_g} grams")
    print(f"Number of Containers: {containers}")
    print(
        f"Wrong conversion (÷1000): {wrong_tonnes} 'tonnes' → {wrong_result} tCO2")
    print(
        f"Correct conversion (÷1,000,000): {correct_tonnes} tonnes → {correct_result} tCO2")

    # Scenario 2: Multiple containers scenario
    container_weight_g2 = 29.2  # grams per container
    containers2 = 14415  # many containers

    total_weight_g = container_weight_g2 * containers2
    total_weight_tonnes = total_weight_g / 1000000
    result2 = total_weight_tonnes * emission_factor

    print(f"\n--- Multiple Containers Scenario ---")
    print(f"Container Weight: {container_weight_g2} grams each")
    print(f"Number of Containers: {containers2}")
    print(
        f"Total Weight: {total_weight_g} grams = {total_weight_tonnes} tonnes")
    print(f"Emissions: {result2} tCO2")

    # Scenario 3: Check if 5495040 could come from wrong calculation
    mystery_result = 5495040.00
    if wrong_result != 0:
        ratio = mystery_result / wrong_result
        print(f"\n--- Mystery Result Analysis ---")
        print(f"Mystery result: {mystery_result}")
        print(f"Our wrong result: {wrong_result}")
        print(f"Ratio: {ratio}")


if __name__ == "__main__":
    print("=== Testing Calculation Issue ===")
    test_basic_calculation()
    test_unit_conversion_scenarios()
