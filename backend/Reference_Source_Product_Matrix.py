import csv
import os


class Reference_Source_Product_Matrix:
    def __init__(self, csv_path):
        self.data = []
        self.header = []
        print(
            f"[DEBUG] Initializing Reference_Source_Product_Matrix with: {csv_path}")
        self._load_csv(csv_path)
        print(f"[DEBUG] Loaded {len(self.data)} rows. Header: {self.header}")

    def _load_csv(self, csv_path):
        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                self.header = reader.fieldnames
                for i, row in enumerate(reader):
                    self.data.append(row)
                    if i < 3:
                        print(f"[DEBUG] Row {i}: {row}")
        except Exception as e:
            print(f"[ERROR] Error loading {csv_path}: {e}")
            self.data = []

    def filter_by_supplier_product_location(self, value):
        column = 'SUPPLIER-PRODUCT-LOCATION'
        print(f"[DEBUG] Filtering for {column} == '{value}'")
        matches = [row for row in self.data if row.get(
            column, '').strip() == value.strip()]
        print(f"[DEBUG] Found {len(matches)} matches.")
        if matches:
            print(f"[DEBUG] First match: {matches[0]}")
        return matches
