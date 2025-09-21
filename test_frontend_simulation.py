#!/usr/bin/env python3

# Test to simulate the frontend calculation and identify the issue

def simulate_frontend_calculation():
    """Simulate the frontend calculation to find the issue"""

    # Test scenarios based on the calculation issue
    print("=== Frontend Calculation Simulation ===")

    # Scenario 1: What if container weight is entered as grams?
    container_weight_grams = 420641.5  # User enters weight in grams
    number_of_containers = 1
    emission_factor = 14.4

    # Current frontend logic (dividing by 1000)
    current_calculation = (container_weight_grams *
                           number_of_containers) / 1000
    current_emissions = current_calculation * emission_factor

    print(f"Scenario 1 - Container weight as grams:")
    print(f"  Container Weight: {container_weight_grams} g")
    print(f"  Number of Containers: {number_of_containers}")
    print(
        f"  Current frontend calc: ({container_weight_grams} * {number_of_containers}) / 1000 = {current_calculation}")
    print(
        f"  Emissions: {current_calculation} * {emission_factor} = {current_emissions}")

    # Scenario 2: Multiple smaller containers
    container_weight_grams2 = 29.2  # grams per container
    number_of_containers2 = 14415

    current_calculation2 = (container_weight_grams2 *
                            number_of_containers2) / 1000
    current_emissions2 = current_calculation2 * emission_factor

    print(f"\nScenario 2 - Multiple containers:")
    print(f"  Container Weight: {container_weight_grams2} g each")
    print(f"  Number of Containers: {number_of_containers2}")
    print(
        f"  Current frontend calc: ({container_weight_grams2} * {number_of_containers2}) / 1000 = {current_calculation2}")
    print(
        f"  Emissions: {current_calculation2} * {emission_factor} = {current_emissions2}")

    # Scenario 3: Check if any of these match 5495040
    target = 5495040.00
    print(f"\nTarget mysterious result: {target}")

    # What if there's an additional multiplication somewhere?
    factor1 = target / current_emissions
    factor2 = target / current_emissions2

    print(f"Factor to get from {current_emissions} to {target}: {factor1}")
    print(f"Factor to get from {current_emissions2} to {target}: {factor2}")

    # Test if it's a unit issue in the calculation chain
    # What if the emission factor is being applied incorrectly?

    # Possible sources of the large number:
    # 1. Double conversion somewhere
    # 2. Wrong units being used
    # 3. Multiple multiplications

    # Check if 5495040 could come from a calculation error
    potential_causes = [
        current_emissions * 907.18,  # Some strange factor
        current_calculation * emission_factor * emission_factor,  # Double application
        (container_weight_grams * number_of_containers) *
        emission_factor,  # No division by 1000
    ]

    print(f"\nPotential error sources:")
    for i, cause in enumerate(potential_causes, 1):
        print(f"  {i}. {cause}")
        if abs(cause - target) < 1000:
            print(f"     *** CLOSE MATCH! ***")


if __name__ == "__main__":
    simulate_frontend_calculation()
