#!/usr/bin/env python3

# Test the miles calculation that might be showing the wrong number

def test_miles_calculation():
    """Test if the large number is from the miles calculation"""

    total_emissions = 6057.2376  # Our correct calculation

    # From line 406 in EmissionSummary.js
    miles_factor = 0.00022
    calculated_miles = total_emissions / miles_factor

    print(f"Total Emissions: {total_emissions} metric tonnes CO2e")
    print(f"Miles Factor: {miles_factor}")
    print(f"Calculated Miles: {calculated_miles}")
    print(f"Formatted Miles: {calculated_miles:.0f}")

    # Check if this matches the mysterious number
    mystery_number = 5495040.00
    print(f"\nMystery Number: {mystery_number}")
    print(f"Difference: {abs(calculated_miles - mystery_number)}")

    if abs(calculated_miles - mystery_number) < 100000:
        print("*** CLOSE MATCH - This might be the miles calculation! ***")

    # What would the total emissions need to be to get exactly 5495040 miles?
    required_emissions = mystery_number * miles_factor
    print(
        f"\nTo get {mystery_number} miles, emissions would need to be: {required_emissions}")


if __name__ == "__main__":
    test_miles_calculation()
