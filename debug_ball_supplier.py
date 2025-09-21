#!/usr/bin/env python3
"""
Debug the specific issue with Ball - Aluminum Cans - Fairfield, CA supplier lookup.
"""

from Components.Reference_Source_Product_Matrix import Reference_Source_Product_Matrix
import requests
import json
import sys
import os

# Add the backend path to import the Reference_Source_Product_Matrix directly
sys.path.append(
    '/Users/mohanganadal/Data Company/Avisk GHG Emisstion Calculator/backend')


# Configuration
BASE_URL = "http://localhost:5002"
API_ENDPOINT = f"{BASE_URL}/api/compute_ghg_emissions"


def debug_supplier_lookup():
    """
    Debug the specific Ball - Aluminum Cans - Fairfield, CA lookup issue.
    """

    print("🔍 Debugging Ball - Aluminum Cans - Fairfield, CA Lookup")
    print("=" * 65)

    # Test the Reference_Source_Product_Matrix class directly
    csv_path = '/Users/mohanganadal/Data Company/Avisk GHG Emisstion Calculator/backend/data/Source_Product_Matrix.csv'
    matrix = Reference_Source_Product_Matrix(csv_path)

    print(f"📁 CSV Path: {csv_path}")
    print(f"📊 Total Records Loaded: {len(matrix.data)}")
    print(f"📋 CSV Headers: {matrix.header}")

    # Test the exact supplier string
    supplier_string = "Ball - Aluminum Cans - Fairfield, CA"
    print(f"\n🎯 Target Supplier: '{supplier_string}'")

    # Test the filter method directly
    matches = matrix.filter_by_supplier_product_location(supplier_string)
    print(f"🔍 Filter Results: {len(matches)} matches found")

    if matches:
        print(f"📋 First Match Data:")
        for key, value in matches[0].items():
            print(f"   {key}: '{value}'")
    else:
        print("❌ No matches found!")

        # Let's check what similar suppliers exist
        print(f"\n🔍 Searching for similar suppliers...")
        ball_suppliers = [row for row in matrix.data if 'Ball' in row.get(
            'SUPPLIER-PRODUCT-LOCATION', '')]
        print(f"📊 Found {len(ball_suppliers)} Ball suppliers:")
        for supplier in ball_suppliers:
            print(f"   - '{supplier.get('SUPPLIER-PRODUCT-LOCATION', '')}'")

    # Test the emission factor method directly
    emission_factor = matrix.get_manufacturing_emissions_factor(
        supplier_string)
    print(f"\n⚡ Direct Method Result: {emission_factor}")

    # Now test via API
    print(f"\n🌐 Testing via API...")

    test_payload = {
        "supplier_data": {
            "Supplier_and_Container": supplier_string,
            "Container_Weight": 800.0,
            "Number_Of_Containers": 10
        },
        "activity_rows": []
    }

    try:
        response = requests.post(
            API_ENDPOINT,
            json=test_payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            manufacturing_details = result.get('manufacturing_details', {})

            print(f"✅ API Call Successful")
            print(f"📊 API Results:")
            print(
                f"   Supplier Emission Factor: {manufacturing_details.get('supplier_emission_factor')}")
            print(
                f"   Emission Factor Source: {manufacturing_details.get('emission_factor_source')}")
            print(
                f"   Manufacturing Emissions: {result.get('manufacturing_emissions', 0):.3f} tonnes")

            # Expected calculation
            expected_emissions = (800.0 * 10 * 14.4) / 1000
            print(f"   Expected Emissions: {expected_emissions:.3f} tonnes")

            actual_factor = manufacturing_details.get(
                'supplier_emission_factor', 0)
            if abs(actual_factor - 14.4) < 0.001:
                print(f"✅ Emission factor is correct!")
            else:
                print(
                    f"❌ Emission factor mismatch: got {actual_factor}, expected 14.4")

        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ API error: {e}")

    # Additional debugging - check exact string matching
    print(f"\n🔍 String Matching Debug:")
    target = supplier_string.strip()
    print(f"Target (stripped): '{target}' (length: {len(target)})")

    for i, row in enumerate(matrix.data):
        stored_value = row.get('SUPPLIER-PRODUCT-LOCATION', '').strip()
        if 'Ball' in stored_value and 'Fairfield' in stored_value:
            print(f"Row {i}: '{stored_value}' (length: {len(stored_value)})")
            print(f"   Exact match: {stored_value == target}")
            print(f"   Character comparison:")
            for j, (c1, c2) in enumerate(zip(target, stored_value)):
                if c1 != c2:
                    print(
                        f"     Position {j}: target='{c1}' (ord {ord(c1)}) vs stored='{c2}' (ord {ord(c2)})")
            if len(target) != len(stored_value):
                print(
                    f"   Length difference: target={len(target)}, stored={len(stored_value)}")


if __name__ == "__main__":
    debug_supplier_lookup()
