#!/usr/bin/env python3

# Test to debug the specific calculation issue

def debug_calculation():
    """Debug the specific calculation issue"""

    # The numbers you mentioned
    material_weight = 420.6415
    emission_factor = 14.4
    incorrect_result = 5495040.00
    correct_result = material_weight * emission_factor

    print(f"Input values:")
    print(f"  Material Weight: {material_weight}")
    print(f"  Emission Factor: {emission_factor}")
    print(f"  Correct Result: {correct_result}")
    print(f"  Incorrect Result: {incorrect_result}")

    # Calculate the factor
    factor = incorrect_result / correct_result
    print(f"  Error Factor: {factor}")

    # Possible explanations:
    print(f"\nPossible explanations:")

    # 1. String concatenation instead of multiplication
    str_concat = str(material_weight) + str(emission_factor)
    print(
        f"  1. String concatenation: '{material_weight}' + '{emission_factor}' = '{str_concat}'")

    # 2. Wrong units somewhere
    print(f"  2. Material weight in wrong units:")
    print(
        f"     - If weight was in grams: {material_weight} * 1000 = {material_weight * 1000}")
    print(
        f"     - Then: {material_weight * 1000} * {emission_factor} = {material_weight * 1000 * emission_factor}")

    # 3. Check if it's related to container calculation
    print(f"  3. Container calculation issues:")
    # If container weight is 420.6415 kg and containers are 1000
    containers = 1000
    if_kg = material_weight * containers * emission_factor
    print(f"     - If 1000 containers of 420.6415 kg each: {if_kg}")

    # 4. Check for JavaScript precision issues
    print(f"  4. Precision/conversion issues:")
    # Convert to integers and back
    as_int = int(material_weight * 1000000) * emission_factor / 1000
    print(f"     - Integer conversion issue: {as_int}")

    # 5. Check if there's a unit mismatch in the display
    print(f"  5. Display unit issues:")
    # If result is actually in grams but displayed as tonnes
    grams_result = correct_result * 1000
    print(f"     - If result in grams: {grams_result}")

    # 6. Most likely: Check if it's a frontend calculation bug
    print(f"  6. Frontend bug possibilities:")

    # Maybe the calculation is being done multiple times
    print(
        f"     - Double calculation: {correct_result} * 907.18 ≈ {correct_result * 907.18}")

    # Maybe there's a conversion factor being applied incorrectly
    # tonnes to kg, mystery factor, kg to lbs
    conversion_factors = [1000, 907.18, 2.20462]
    for cf in conversion_factors:
        result = correct_result * cf
        print(f"     - With factor {cf}: {result}")
        if abs(result - incorrect_result) < 1000:
            print(f"       *** POTENTIAL MATCH ***")


if __name__ == "__main__":
    debug_calculation()
