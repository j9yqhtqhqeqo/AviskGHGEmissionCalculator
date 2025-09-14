import csv
import os


def test_csv_reading():
    csv_path = os.path.join(os.path.dirname(__file__), 'Supplier_List.csv')
    print(f"Attempting to read CSV from: {csv_path}")

    try:
        with open(csv_path, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            print(f"CSV Header: {header}")

            suppliers = []
            for row in csv_reader:
                if row:
                    supplier = row[0].strip('"').strip()
                    suppliers.append(supplier)
                    print(f"Added supplier: {supplier}")

            print(f"Total suppliers found: {len(suppliers)}")
            print(f"Suppliers: {suppliers}")
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")


if __name__ == "__main__":
    test_csv_reading()
