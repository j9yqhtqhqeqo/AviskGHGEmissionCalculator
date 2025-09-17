import csv


class Reference_Unit_Conversion:
    def __init__(self, csv_path):
        self.matrix = {}
        self.row_headers = []
        self.col_headers = []
        self.load_matrix(csv_path)

    def load_matrix(self, csv_path):
        print(f"Loading Reference - Unit Conversion.csv from: {csv_path}")
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            rows = list(reader)
            # Find the start of the matrix: look for 'From Unit' in first column
            matrix_start_row = None
            for i, row in enumerate(rows):
                if row and row[0].strip() == 'From Unit':
                    matrix_start_row = i
                    break
            if matrix_start_row is None:
                raise ValueError("Could not find 'From Unit' header in CSV.")
            # The next row is the column headers
            self.col_headers = [h.strip()
                                for h in rows[matrix_start_row][1:] if h.strip()]
            # The following rows are the matrix data until a blank row or non-matrix section
            i = matrix_start_row + 1
            while i < len(rows):
                row = rows[i]
                if not row or not row[0].strip() or row[0].strip() == '':
                    break
                row_header = row[0].strip()
                self.row_headers.append(row_header)
                for j, value in enumerate(row[1:len(self.col_headers)+1]):
                    col_header = self.col_headers[j]
                    if row_header not in self.matrix:
                        self.matrix[row_header] = {}
                    self.matrix[row_header][col_header] = value.strip(
                    ) if value else ''
                i += 1
            print(
                f"Loaded unit conversion matrix: {len(self.row_headers)} rows, {len(self.col_headers)} columns.")

    def get_conversion(self, from_unit, to_unit):
        # Case-insensitive lookup
        from_unit = from_unit.strip().lower()
        to_unit = to_unit.strip().lower()
        for row_header in self.row_headers:
            if row_header.lower() == from_unit:
                for col_header in self.col_headers:
                    if col_header.lower() == to_unit:
                        return self.matrix[row_header][col_header]
        return None

# Reference_EF_Fuel_Use_CO2: for Reference - EF Fuel Use CO2.csv


class Reference_EF_Fuel_Use_CO2:
    def __init__(self, csv_path):
        self.data = []
        self.header = []
        self.load_csv(csv_path)

    def load_csv(self, csv_path):
        print(f"Loading Reference - EF Fuel Use CO2.csv from: {csv_path}")
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            self.header = reader.fieldnames
            print(f"CSV Header: {self.header}")
            count = 0
            for row in reader:
                # Only add rows with a Fuel value
                if row.get('Fuel'):
                    self.data.append(row)
                    count += 1
            print(f"Loaded {count} rows with 'Fuel'.")

    def get_by_fuel_and_region(self, fuel, region):
        # Case-insensitive match for both fuel and region
        results = [
            row for row in self.data
            if row['Fuel'].strip().lower() == fuel.strip().lower()
            and row['Region'].strip().lower() == region.strip().lower()
        ]
        print(
            f"Query for fuel='{fuel}', region='{region}' found {len(results)} result(s).")
        return results

# Reference_EF_Fuel_Use_CH4_N2O: for Reference - EF Fuel Use CH4 N2O.csv


class Reference_EF_Fuel_Use_CH4_N2O:
    def __init__(self, csv_path):
        self.data = []
        self.header = []
        self.load_csv(csv_path)

    def load_csv(self, csv_path):
        print(f"Loading Reference - EF Fuel Use CH4 N2O.csv from: {csv_path}")
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            self.header = reader.fieldnames
            print(f"CSV Header: {self.header}")
            count = 0
            for row in reader:
                # Only add rows with a Transport and Fuel value
                if row.get('Transport and Fuel'):
                    self.data.append(row)
                    count += 1
            print(f"Loaded {count} rows with 'Transport and Fuel'.")

    def get_by_transport_and_region(self, transport_and_fuel, region):
        # Case-insensitive match for both transport_and_fuel and region
        results = [
            row for row in self.data
            if row['Transport and Fuel'].strip().lower() == transport_and_fuel.strip().lower()
            and row['Region'].strip().lower() == region.strip().lower()
        ]
        print(
            f"Query for transport_and_fuel='{transport_and_fuel}', region='{region}' found {len(results)} result(s).")
        return results
# Reference_EF_Road: for Reference_EF_Road.csv


class Reference_EF_Road:
    def __init__(self, csv_path):
        self.data = []
        self.header = []
        self.load_csv(csv_path)

    def load_csv(self, csv_path):
        print(f"Loading Reference_EF_Road.csv from: {csv_path}")
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            self.header = reader.fieldnames
            print(f"CSV Header: {self.header}")
            count = 0
            for row in reader:
                # Only add rows with a Vehicle and Fuel and Vehicle Year value
                if row.get('Vehicle and Fuel and Vehicle Year'):
                    self.data.append(row)
                    count += 1
            print(
                f"Loaded {count} rows with 'Vehicle and Fuel and Vehicle Year'.")

    def get_by_vehicle_and_region(self, vehicle_fuel_year, region):
        # Case-insensitive match for both vehicle_fuel_year and region
        results = [
            row for row in self.data
            if row['Vehicle and Fuel and Vehicle Year'].strip().lower() == vehicle_fuel_year.strip().lower()
            and row['Region'].strip().lower() == region.strip().lower()
        ]
        print(
            f"Query for vehicle_fuel_year='{vehicle_fuel_year}', region='{region}' found {len(results)} result(s).")
        return results


class Reference_EF_Freight_CH4_NO2:
    def __init__(self, csv_path):
        self.data = []
        self.header = []
        self.load_csv(csv_path)

    def load_csv(self, csv_path):
        print(f"Loading Reference_EF_Freight_CH4_NO2.csv from: {csv_path}")
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            self.header = reader.fieldnames
            print(f"CSV Header: {self.header}")
            count = 0
            for row in reader:
                # Only add rows with a Vehicle Type value
                if row.get('Vehicle Type'):
                    self.data.append(row)
                    count += 1
            print(f"Loaded {count} rows with 'Vehicle Type'.")

    def get_by_vehicle_and_region(self, vehicle_type, region):
        # Case-insensitive match for both vehicle_type and region
        results = [
            row for row in self.data
            if row['Vehicle Type'].strip().lower() == vehicle_type.strip().lower()
            and row['Region'].strip().lower() == region.strip().lower()
        ]
        print(
            f"Query for vehicle_type='{vehicle_type}', region='{region}' found {len(results)} result(s).")
        return results


class Reference_EF_Public:
    def __init__(self, csv_path):
        self.data = []
        self.header = []
        self.load_csv(csv_path)

    def load_csv(self, csv_path):
        print(f"Loading Reference_EF_Public.csv from: {csv_path}")
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            self.header = reader.fieldnames
            print(f"CSV Header: {self.header}")
            count = 0
            for row in reader:
                # Only add rows with a Vehicle and Type value
                if row.get('Vehicle and Type'):
                    self.data.append(row)
                    count += 1
            print(f"Loaded {count} rows with 'Vehicle and Type'.")

    def get_by_vehicle_and_region(self, vehicle_type, region):
        # Case-insensitive match for both vehicle_type and region
        results = [
            row for row in self.data
            if row['Vehicle and Type'].strip().lower() == vehicle_type.strip().lower()
            and row['Region'].strip().lower() == region.strip().lower()
        ]
        print(
            f"Query for vehicle_type='{vehicle_type}', region='{region}' found {len(results)} result(s).")
        return results

# Reference_EF_Freight_CO2: similar to Reference_EF_Public but for Reference_EF_Freight_CO2.csv


class Reference_EF_Freight_CO2:
    def __init__(self, csv_path):
        self.data = []
        self.header = []
        self.load_csv(csv_path)

    def load_csv(self, csv_path):
        print(f"Loading Reference_EF_Freight_CO2.csv from: {csv_path}")
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            self.header = reader.fieldnames
            print(f"CSV Header: {self.header}")
            count = 0
            for row in reader:
                # Only add rows with a Vehicle and Size value
                if row.get('Vehicle and Size'):
                    self.data.append(row)
                    count += 1
            print(f"Loaded {count} rows with 'Vehicle and Size'.")

    def get_by_vehicle_and_region(self, vehicle_size, region):
        # Case-insensitive match for both vehicle_size and region
        results = [
            row for row in self.data
            if row['Vehicle and Size'].strip().lower() == vehicle_size.strip().lower()
            and row['Region'].strip().lower() == region.strip().lower()
        ]
        print(
            f"Query for vehicle_size='{vehicle_size}', region='{region}' found {len(results)} result(s).")
        return results
