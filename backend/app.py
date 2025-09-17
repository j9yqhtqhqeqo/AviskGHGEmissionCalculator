# ...existing code...
# ...existing code...
# --- Place this after reference_ef_freight is initialized ---


from flask import Flask, jsonify, request
import csv
import os
from flask_cors import CORS
import json
from Components.Supplier_Input import Supplier_Input
from Components.reference_ef import Reference_EF_Public, Reference_EF_Freight_CO2, Reference_EF_Freight_CH4_NO2, Reference_EF_Road, Reference_EF_Fuel_Use_CH4_N2O, Reference_EF_Fuel_Use_CO2, Reference_Unit_Conversion
from Components.reference_lookups import ReferenceLookup
from Components.Reference_Source_Product_Matrix import Reference_Source_Product_Matrix


# Initialize Flask app and CORS at the top
# Initialize Flask app and CORS at the top
app = Flask(__name__)
CORS(app)

# --- Reference - Lookups.csv Lookups ---
lookups_csv_path = os.path.join(
    os.path.dirname(__file__), 'data', 'Reference - Lookups.csv')
lookup_columns = [
    'Region',
    'Mode of Transport',
    'Type of Activity Data',
    'Scope',
    'Units ',
    'IPCC GWP Version',
    'Activity Data Columns',
    'Unit of Fuel Amount'
]
reference_lookups = {col: ReferenceLookup(
    lookups_csv_path, col) for col in lookup_columns}
# API endpoint for Reference_Unit_Conversion


# --- API endpoints for Reference - Lookups.csv ---
@app.route('/api/lookup/<lookup_name>', methods=['GET'])
def get_lookup_values(lookup_name):
    lookup_map = {
        'region': 'Region',
        'mode_of_transport': 'Mode of Transport',
        'type_of_activity_data': 'Type of Activity Data',
        'scope': 'Scope',
        'units': 'Units ',
        'ipcc_gwp_version': 'IPCC GWP Version',
        'activity_data_columns': 'Activity Data Columns',
        'unit_of_fuel_amount': 'Unit of Fuel Amount',
    }
    col = lookup_map.get(lookup_name.lower())
    if not col or col not in reference_lookups:
        return jsonify({'error': f'Unknown lookup: {lookup_name}'}), 404
    values = reference_lookups[col].get_all()
    return jsonify({'lookup': lookup_name, 'values': values})

# Explicit endpoint for Scope lookup (optional, for clarity)


@app.route('/api/lookup/scope', methods=['GET'])
def get_scope_lookup():
    values = reference_lookups['Scope'].get_all()
    return jsonify({'lookup': 'scope', 'values': values})

# Explicit endpoint for Unit of Fuel Amount lookup (optional, for clarity)
@app.route('/api/lookup/unit_of_fuel_amount', methods=['GET'])
def get_unit_of_fuel_amount_lookup():
    values = reference_lookups['Unit of Fuel Amount'].get_all()
    return jsonify({'lookup': 'unit_of_fuel_amount', 'values': values})


@app.route('/api/lookup/<lookup_name>/value', methods=['GET'])
def get_lookup_by_value(lookup_name):
    from flask import request
    value = request.args.get('value', '')
    lookup_map = {
        'region': 'Region',
        'mode_of_transport': 'Mode of Transport',
        'type_of_activity_data': 'Type of Activity Data',
        'scope': 'Scope',
        'units': 'Units ',
        'ipcc_gwp_version': 'IPCC GWP Version',
        'activity_data_columns': 'Activity Data Columns',
        'unit_of_fuel_amount': 'Unit of Fuel Amount',
    }
    col = lookup_map.get(lookup_name.lower())
    if not col or col not in reference_lookups:
        return jsonify({'error': f'Unknown lookup: {lookup_name}'}), 404
    if not value:
        return jsonify({'error': 'Missing value parameter'}), 400
    results = reference_lookups[col].get_by_value(value)
    return jsonify({'lookup': lookup_name, 'value': value, 'results': results})


# Initialize Reference_Unit_Conversion instance (load once at startup)
unit_conversion_csv_path = os.path.join(
    os.path.dirname(__file__), 'data', 'Reference - Unit Conversion.csv')
reference_unit_conversion = Reference_Unit_Conversion(unit_conversion_csv_path)

# API endpoint for Reference_Unit_Conversion


@app.route('/api/unit_conversion', methods=['GET'])
def get_unit_conversion():
    from flask import request
    from_unit = request.args.get('from_unit', '')
    to_unit = request.args.get('to_unit', '')
    print(
        f"Received API request for unit conversion: from '{from_unit}' to '{to_unit}'")
    if not from_unit or not to_unit:
        print("Missing from_unit or to_unit in query.")
        return jsonify({'error': 'Both from_unit and to_unit query parameters are required'}), 400
    value = reference_unit_conversion.get_conversion(from_unit, to_unit)
    if value is None or value == '':
        print(
            f"No conversion value found for from_unit: {from_unit}, to_unit: {to_unit}")
        return jsonify({'error': f'No conversion value found for from_unit: {from_unit}, to_unit: {to_unit}'}), 404
    print(
        f"Returning conversion value: {value} for from_unit: {from_unit}, to_unit: {to_unit}")
    return jsonify({'from_unit': from_unit, 'to_unit': to_unit, 'value': value})


# Initialize Reference_EF_Fuel_Use_CO2 instance (load once at startup)
ef_fuel_use_co2_csv_path = os.path.join(
    os.path.dirname(__file__), 'data', 'Reference - EF Fuel Use CO2.csv')
reference_ef_fuel_use_co2 = Reference_EF_Fuel_Use_CO2(ef_fuel_use_co2_csv_path)

# API endpoint for Reference_EF_Fuel_Use_CO2


@app.route('/api/ef_fuel_use_co2', methods=['GET'])
def get_ef_fuel_use_co2_by_fuel_and_region():
    print("[DEBUG] /api/ef_fuel_use_co2 endpoint called")
    from flask import request
    fuel = request.args.get('fuel', '')
    region = request.args.get('region', '')
    print(
        f"Received API request for fuel: '{fuel}', region: '{region}' (Fuel Use CO2)")
    if not fuel or not region:
        print("Missing fuel or region in query.")
        return jsonify({'error': 'Both fuel and region query parameters are required'}), 400
    results = reference_ef_fuel_use_co2.get_by_fuel_and_region(fuel, region)
    if not results:
        print(
            f"No data found for fuel: {fuel}, region: {region}")
        return jsonify({'error': f'No data found for fuel: {fuel}, region: {region}'}), 404
    print(
        f"Returning {len(results)} result(s) for fuel: {fuel}, region: {region}")
    return jsonify({'results': results})


# Initialize Reference_EF_Fuel_Use_CH4_N2O instance (load once at startup)
ef_fuel_use_ch4_n2o_csv_path = os.path.join(
    os.path.dirname(__file__), 'data', 'Reference - EF Fuel Use CH4 N2O.csv')
reference_ef_fuel_use_ch4_n2o = Reference_EF_Fuel_Use_CH4_N2O(
    ef_fuel_use_ch4_n2o_csv_path)

# API endpoint for Reference_EF_Fuel_Use_CH4_N2O


@app.route('/api/ef_fuel_use_ch4_n2o', methods=['GET'])
def get_ef_fuel_use_ch4_n2o_by_transport_and_region():
    from flask import request
    transport_and_fuel = request.args.get('transport_and_fuel', '')
    region = request.args.get('region', '')
    print(
        f"Received API request for transport_and_fuel: '{transport_and_fuel}', region: '{region}' (Fuel Use CH4 N2O)")
    if not transport_and_fuel or not region:
        print("Missing transport_and_fuel or region in query.")
        return jsonify({'error': 'Both transport_and_fuel and region query parameters are required'}), 400
    results = reference_ef_fuel_use_ch4_n2o.get_by_transport_and_region(
        transport_and_fuel, region)
    if not results:
        print(
            f"No data found for transport_and_fuel: {transport_and_fuel}, region: {region}")
        return jsonify({'error': f'No data found for transport_and_fuel: {transport_and_fuel}, region: {region}'}), 404
    print(
        f"Returning {len(results)} result(s) for transport_and_fuel: {transport_and_fuel}, region: {region}")
    return jsonify({'results': results})


# Initialize Reference_EF_Road instance (load once at startup)
ef_road_csv_path = os.path.join(
    os.path.dirname(__file__), 'data', 'Reference_EF_Road.csv')
reference_ef_road = Reference_EF_Road(ef_road_csv_path)

# API endpoint for Reference_EF_Road


@app.route('/api/ef_road', methods=['GET'])
def get_ef_road_by_vehicle_and_region():
    from flask import request
    vehicle_fuel_year = request.args.get('vehicle_fuel_year', '')
    region = request.args.get('region', '')
    print(
        f"Received API request for vehicle_fuel_year: '{vehicle_fuel_year}', region: '{region}' (Road)")
    if not vehicle_fuel_year or not region:
        print("Missing vehicle_fuel_year or region in query.")
        return jsonify({'error': 'Both vehicle_fuel_year and region query parameters are required'}), 400
    results = reference_ef_road.get_by_vehicle_and_region(
        vehicle_fuel_year, region)
    if not results:
        print(
            f"No data found for vehicle_fuel_year: {vehicle_fuel_year}, region: {region}")
        return jsonify({'error': f'No data found for vehicle_fuel_year: {vehicle_fuel_year}, region: {region}'}), 404
    print(
        f"Returning {len(results)} result(s) for vehicle_fuel_year: {vehicle_fuel_year}, region: {region}")
    return jsonify({'results': results})


# Initialize Reference_EF_Public instance (load once at startup)
ef_csv_path = os.path.join(os.path.dirname(
    __file__), 'data', 'Reference_EF_Public.csv')
reference_ef = Reference_EF_Public(ef_csv_path)


# Initialize Reference_EF_Freight_CO2 instance (load once at startup)
ef_freight_csv_path = os.path.join(os.path.dirname(
    __file__), 'data', 'Reference_EF_Freight_CO2.csv')
reference_ef_freight = Reference_EF_Freight_CO2(ef_freight_csv_path)

# Initialize Reference_EF_Freight_CH4_NO2 instance (load once at startup)
ef_freight_ch4_no2_csv_path = os.path.join(
    os.path.dirname(__file__), 'data', 'Reference_EF_Freight_CH4_NO2.csv')
reference_ef_freight_ch4_no2 = Reference_EF_Freight_CH4_NO2(
    ef_freight_ch4_no2_csv_path)

# API endpoint for Reference_EF_Freight_CH4_NO2


@app.route('/api/ef_freight_ch4_no2', methods=['GET'])
def get_ef_freight_ch4_no2_by_vehicle_and_region():
    from flask import request
    vehicle_type = request.args.get('vehicle_type', '')
    region = request.args.get('region', '')
    print(
        f"Received API request for vehicle_type: '{vehicle_type}', region: '{region}' (CH4/NO2)")
    if not vehicle_type or not region:
        print("Missing vehicle_type or region in query.")
        return jsonify({'error': 'Both vehicle_type and region query parameters are required'}), 400
    results = reference_ef_freight_ch4_no2.get_by_vehicle_and_region(
        vehicle_type, region)
    if not results:
        print(
            f"No data found for vehicle_type: {vehicle_type}, region: {region}")
        return jsonify({'error': f'No data found for vehicle_type: {vehicle_type}, region: {region}'}), 404
    print(
        f"Returning {len(results)} result(s) for vehicle_type: {vehicle_type}, region: {region}")
    return jsonify({'results': results})

 # API endpoint for Reference_EF_Freight_CO2 (renamed to include co2)


@app.route('/api/ef_freight_co2', methods=['GET'])
def get_ef_freight_co2_by_vehicle_and_region():
    from flask import request
    vehicle_size = request.args.get('vehicle_size', '')
    region = request.args.get('region', '')
    print(
        f"Received API request for vehicle_size: '{vehicle_size}', region: '{region}'")
    if not vehicle_size or not region:
        print("Missing vehicle_size or region in query.")
        return jsonify({'error': 'Both vehicle_size and region query parameters are required'}), 400
    results = reference_ef_freight.get_by_vehicle_and_region(
        vehicle_size, region)
    if not results:
        print(
            f"No data found for vehicle_size: {vehicle_size}, region: {region}")
        return jsonify({'error': f'No data found for vehicle_size: {vehicle_size}, region: {region}'}), 404
    print(
        f"Returning {len(results)} result(s) for vehicle_size: {vehicle_size}, region: {region}")
    return jsonify({'results': results})


@app.route('/api/ef', methods=['GET'])
def get_ef_by_vehicle_and_region():
    from flask import request
    vehicle_type = request.args.get('vehicle_type', '')
    region = request.args.get('region', '')
    print(
        f"Received API request for vehicle_type: '{vehicle_type}', region: '{region}'")
    if not vehicle_type or not region:
        print("Missing vehicle_type or region in query.")
        return jsonify({'error': 'Both vehicle_type and region query parameters are required'}), 400
    results = reference_ef.get_by_vehicle_and_region(vehicle_type, region)
    if not results:
        print(
            f"No data found for vehicle_type: {vehicle_type}, region: {region}")
        return jsonify({'error': f'No data found for vehicle_type: {vehicle_type}, region: {region}'}), 404
    print(
        f"Returning {len(results)} result(s) for vehicle_type: {vehicle_type}, region: {region}")
    return jsonify({'results': results})


@app.route('/')
def home():
    return jsonify({'message': 'Avisk GHG Calculator Flask backend is running.'})


@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = []
    csv_path = os.path.join(os.path.dirname(__file__),
                            'data', 'Supplier_List.csv')

    print(f"Attempting to read CSV from: {csv_path}")

    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            # Skip header row
            header = next(csv_reader)
            print(f"CSV Header: {header}")

            for row in csv_reader:
                if row:  # Check if row is not empty
                    # Remove quotes and trim whitespace
                    supplier = row[0].strip('"').strip()
                    suppliers.append(supplier)
                    print(f"Added supplier: {supplier}")

        result = {'suppliers': suppliers}
        print(f"Total suppliers: {len(suppliers)}")
        return jsonify(result)
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return jsonify({'error': str(e)}), 500


# --- Load Reference_Source_Product_Matrix at startup ---
source_product_matrix_csv_path = os.path.join(
    os.path.dirname(__file__), 'data', 'Source_Product_Matrix.csv')
reference_source_product_matrix = Reference_Source_Product_Matrix(
    source_product_matrix_csv_path)

# --- API endpoint: source_product_matrix ---


@app.route('/api/source_product_matrix', methods=['GET'])
def get_source_product_matrix():
    supplier = request.args.get('supplier', '')
    product = request.args.get('product', '')
    location = request.args.get('location', '')
    if not supplier or not product or not location:
        return jsonify({'error': 'Missing supplier, product, or location parameter'}), 400
    supplier_product_location = f"{supplier} - {product} - {location}"
    print(
        f"[DEBUG] /api/source_product_matrix called with: {supplier_product_location}")
    results = reference_source_product_matrix.filter_by_supplier_product_location(
        supplier_product_location)
    return jsonify({'results': results})


# --- API endpoint: compute_ghg_emissions ---
@app.route('/api/compute_ghg_emissions', methods=['POST'])
def compute_ghg_emissions():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing JSON body'}), 400

        # Extract and map fields to Supplier_Input
        supplier_input = Supplier_Input(
            Supplier_and_Container=data.get('Supplier_and_Container', ''),
            Container_Weight=float(data.get('Container_Weight', 0)),
            Number_Of_Containers=int(data.get('Number_Of_Containers', 0)),
            Source_Description=data.get('Source_Description', ''),
            Region=data.get('Region', ''),
            Mode_of_Transport=data.get('Mode_of_Transport', ''),
            Scope=data.get('Scope', ''),
            Type_Of_Activity_Data=data.get('Type_Of_Activity_Data', ''),
            Vehicle_Type=data.get('Vehicle_Type'),
            Distance_Travelled=float(data['Distance_Travelled']) if data.get(
                'Distance_Travelled') is not None else None,
            Total_Weight_Of_Freight_InTonne=float(data['Total_Weight_Of_Freight_InTonne']) if data.get(
                'Total_Weight_Of_Freight_InTonne') is not None else None,
            Num_Of_Passenger=int(data['Num_Of_Passenger']) if data.get(
                'Num_Of_Passenger') is not None else None,
            Units_of_Measurement=data.get('Units_of_Measurement'),
            Fuel_Used=data.get('Fuel_Used'),
            Fuel_Amount=float(data['Fuel_Amount']) if data.get(
                'Fuel_Amount') is not None else None,
            Unit_Of_Fuel_Amount=data.get('Unit_Of_Fuel_Amount')
        )

        # Placeholder: actual GHG calculation logic goes here
        # For now, just echo the parsed input
        return jsonify({'status': 'success', 'input': supplier_input.__dict__})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get unique Vehicle and Size for a given region and mode of transport


@app.route('/api/vehicle_and_size', methods=['GET'])
def get_vehicle_and_size_by_region_and_mode():
    region = request.args.get('region', '')
    mode_of_transport = request.args.get('mode_of_transport', '')
    if not region or not mode_of_transport:
        return jsonify({'error': 'Both region and mode_of_transport query parameters are required'}), 400
    # Filter rows from reference_ef_freight by region and mode of transport
    matches = [
        row['Vehicle and Size']
        for row in reference_ef_freight.data
        if row.get('Region', '').strip().lower() == region.strip().lower()
        and row.get('Mode of Transport', '').strip().lower() == mode_of_transport.strip().lower()
        and row.get('Vehicle and Size')
    ]
    # Return unique values, sorted
    unique_vehicle_and_size = sorted(list(set(matches)))
    return jsonify({'region': region, 'mode_of_transport': mode_of_transport, 'vehicle_and_size': unique_vehicle_and_size})

# API endpoint to get unique fuel types


@app.route('/api/fuel_types', methods=['GET'])
def get_fuel_types():
    try:
        # Get unique fuel types from reference_ef_fuel_use_co2
        fuel_types = sorted(list(set([
            row.get('Fuel', '')
            for row in reference_ef_fuel_use_co2.data
            if row.get('Fuel', '').strip()
        ])))
        return jsonify({'fuel_types': fuel_types})
    except Exception as e:
        print(f"Error getting fuel types: {str(e)}")
        return jsonify({'error': 'Failed to retrieve fuel types'}), 500
#

# print('[DEBUG] Registered endpoints:')
# for rule in app.url_map.iter_rules():
#     print(rule)


if __name__ == '__main__':
    app.run(debug=True)
