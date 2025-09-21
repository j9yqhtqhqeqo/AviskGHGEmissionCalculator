import csv
import os


class Reference_Source_Product_Matrix:
    def __init__(self, csv_path):
        self.data = []
        self.header = []
        self._load_csv(csv_path)

    def _load_csv(self, csv_path):
        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                self.header = reader.fieldnames
                for i, row in enumerate(reader):
                    self.data.append(row)
        except Exception as e:
            self.data = []

    def filter_by_supplier_product_location(self, value):
        column = 'SUPPLIER-PRODUCT-LOCATION'
        matches = [row for row in self.data if row.get(
            column, '').strip() == value.strip()]
        return matches

    def get_manufacturing_emissions_factor(self, supplier_product_location):
        """
        Get the Manufacturing Emissions Factor for a given SUPPLIER-PRODUCT-LOCATION.
        Returns the emission factor as float, or None if not found.
        """
        try:
            matches = self.filter_by_supplier_product_location(
                supplier_product_location)
            if matches:
                # Get the first match (should be unique per supplier-product-location)
                first_match = matches[0]
                emission_factor_str = first_match.get(
                    'Manufacturing Emissions Factor (tCO2 per 1t material)', '')

                if emission_factor_str and emission_factor_str.strip():
                    # Convert to float, handling potential formatting issues
                    return float(emission_factor_str.strip())

            return None
        except (ValueError, TypeError) as e:
            print(
                f"Error converting emission factor to float for '{supplier_product_location}': {e}")
            return None
