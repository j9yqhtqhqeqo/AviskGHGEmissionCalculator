import csv
import os


class ReferenceLookup:
    def __init__(self, csv_path, lookup_column):
        self.lookup_column = lookup_column
        self.data = []
        self.header = []
        self.load_csv(csv_path)

    def load_csv(self, csv_path):
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            self.header = reader.fieldnames
            count = 0
            for row in reader:
                if row.get(self.lookup_column):
                    self.data.append(row)
                    count += 1

    def get_all(self):
        # Return all unique values for the lookup column
        return sorted(set(row[self.lookup_column] for row in self.data if row[self.lookup_column]))

    def get_by_value(self, value):
        # Return all rows matching the lookup value (case-insensitive)
        return [row for row in self.data if row[self.lookup_column].strip().lower() == value.strip().lower()]
