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
