#!/usr/bin/env python3

# Test the fix for the unit conversion issue

def test_unit_conversion_fix():
    """Test the corrected unit conversion"""

    print("=== Testing Unit Conversion Fix ===")

    # Your example values
    container_weight_grams = 420641.5  # Container weight in grams
    number_of_containers = 1
    supplier_emission_factor = 14.4  # tCO2e per tonne

    print(f"Input values:")
    print(f"  Container Weight: {container_weight_grams} grams")
    print(f"  Number of Containers: {number_of_containers}")
    print(
        f"  Supplier Emission Factor: {supplier_emission_factor} tCO2e/tonne")

    # OLD (incorrect) calculation: divide by 1000 (converts grams to kg, not tonnes)
    old_total_weight = (container_weight_grams * number_of_containers) / 1000
    old_manufacturing_emissions = old_total_weight * supplier_emission_factor

    print(f"\nOLD (incorrect) calculation:")
    print(
        f"  Total Weight: ({container_weight_grams} * {number_of_containers}) / 1000 = {old_total_weight} kg (WRONG UNIT)")
    print(
        f"  Manufacturing Emissions: {old_total_weight} * {supplier_emission_factor} = {old_manufacturing_emissions} (WRONG)")

    # NEW (correct) calculation: divide by 1,000,000 (converts grams to tonnes)
    new_total_weight = (container_weight_grams *
                        number_of_containers) / 1000000
    new_manufacturing_emissions = new_total_weight * supplier_emission_factor

    print(f"\nNEW (correct) calculation:")
    print(
        f"  Total Weight: ({container_weight_grams} * {number_of_containers}) / 1,000,000 = {new_total_weight} tonnes")
    print(
        f"  Manufacturing Emissions: {new_total_weight} * {supplier_emission_factor} = {new_manufacturing_emissions} tCO2e")

    # Display values for the table
    print(f"\nTable display values:")
    print(f"  Total Material Weight (g): {new_total_weight * 1000000:,.0f}")
    print(
        f"  Total Material Weight (short tons): {new_total_weight * 1.10231:.4f}")
    print(
        f"  Manufacturing Emissions: {new_manufacturing_emissions:.2f} tCO2e")

    # Check if this matches the expected result
    expected_result = 6.0572376  # For 420.6415 grams = 0.4206415 tonnes
    print(f"\nExpected result: {expected_result:.7f} tCO2e")
    print(f"Actual result: {new_manufacturing_emissions:.7f} tCO2e")
    print(
        f"Match: {'✓' if abs(new_manufacturing_emissions - expected_result) < 0.0001 else '✗'}")


if __name__ == "__main__":
    test_unit_conversion_fix()
