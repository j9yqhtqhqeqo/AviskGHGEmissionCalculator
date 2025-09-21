#!/usr/bin/env python3

# Comprehensive test to verify the entire calculation chain

def test_complete_calculation_chain():
    """Test the complete calculation chain to find the 5495040 error"""

    print("=== Complete Calculation Chain Test ===")

    # Simulate the inputs based on your scenario
    container_weight_grams = 420641.5  # Example: user enters this in grams
    number_of_containers = 1
    supplier_emission_factor = 14.4

    print(f"Inputs:")
    print(f"  Container Weight: {container_weight_grams} grams")
    print(f"  Number of Containers: {number_of_containers}")
    print(
        f"  Supplier Emission Factor: {supplier_emission_factor} tCO2e/tonne")

    # Step 1: Frontend calculates total material weight
    # Current frontend logic: (containerWeight * numberOfContainers) / 1000
    total_material_weight_tonnes = (
        container_weight_grams * number_of_containers) / 1000
    print(f"\nStep 1 - Total Material Weight:")
    print(f"  ({container_weight_grams} * {number_of_containers}) / 1000 = {total_material_weight_tonnes} tonnes")

    # Step 2: Calculate manufacturing emissions
    manufacturing_emissions = total_material_weight_tonnes * supplier_emission_factor
    print(f"\nStep 2 - Manufacturing Emissions:")
    print(f"  {total_material_weight_tonnes} * {supplier_emission_factor} = {manufacturing_emissions} tCO2e")

    # Step 3: Check various display calculations that might be wrong
    print(f"\nStep 3 - Display Calculations:")

    # Weight in kg (for display)
    weight_kg = total_material_weight_tonnes * 1000
    print(f"  Weight in kg: {weight_kg}")

    # WRONG short tons calculation (current bug)
    wrong_short_tons = (total_material_weight_tonnes / 1000) * 1.10231
    print(
        f"  WRONG short tons: ({total_material_weight_tonnes} / 1000) * 1.10231 = {wrong_short_tons}")

    # CORRECT short tons calculation (fixed)
    correct_short_tons = total_material_weight_tonnes * 1.10231
    print(
        f"  CORRECT short tons: {total_material_weight_tonnes} * 1.10231 = {correct_short_tons}")

    # Check if any of these calculations could lead to 5495040
    mystery_number = 5495040.0

    # Test scenarios that might create the large number
    scenarios = [
        ("Manufacturing emissions in grams", manufacturing_emissions * 1000000),
        ("Weight in grams * emission factor",
         container_weight_grams * supplier_emission_factor),
        ("Wrong calculation: weight_kg * emission_factor",
         weight_kg * supplier_emission_factor),
        ("Manufacturing emissions * wrong factor",
         manufacturing_emissions * 907.18),
        ("Weight * emission factor without conversion", container_weight_grams *
         number_of_containers * supplier_emission_factor),
    ]

    print(f"\nStep 4 - Testing scenarios for mystery number {mystery_number}:")
    for description, value in scenarios:
        print(f"  {description}: {value}")
        if abs(value - mystery_number) < 100000:
            print(f"    *** POTENTIAL MATCH! ***")
        elif abs(value - mystery_number) < 1000000:
            print(f"    *** CLOSE! ***")


def test_specific_ball_fairfield():
    """Test the specific Ball - Fairfield, CA scenario"""
    print(f"\n=== Ball Fairfield Specific Test ===")

    # From the CSV, Ball - Fairfield, CA has emission factor 14.4
    emission_factor = 14.4

    # If total material weight is 420.6415 tonnes
    material_weight = 420.6415

    correct_result = material_weight * emission_factor
    mystery_result = 5495040.0

    print(f"Material Weight: {material_weight} tonnes")
    print(f"Emission Factor: {emission_factor} tCO2e/tonne")
    print(f"Correct Result: {correct_result} tCO2e")
    print(f"Mystery Result: {mystery_result}")
    print(f"Error Factor: {mystery_result / correct_result}")

    # What if the calculation is being done with wrong units?
    # Maybe the weight is being treated as grams instead of tonnes?
    if_grams = (material_weight * 1000000) / 1000 * \
        emission_factor  # Convert to grams, then back
    print(f"If weight treated as grams then converted: {if_grams}")

    # Maybe there's a JavaScript precision issue?
    # JavaScript sometimes has floating point precision issues
    print(f"Checking JavaScript-like calculations:")
    print(
        f"  {material_weight} * {emission_factor} = {material_weight * emission_factor}")


if __name__ == "__main__":
    test_complete_calculation_chain()
    test_specific_ball_fairfield()
