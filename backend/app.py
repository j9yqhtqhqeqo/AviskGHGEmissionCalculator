# ...existing code...
# ...existing code...
# --- Place this after reference_ef_freight is initialized ---


from flask import Flask, jsonify, request
import csv
import os
import logging
from flask_cors import CORS
import json
from Components.Supplier_Input import Supplier_Input
from Components.reference_ef import Reference_EF_Public, Reference_EF_Freight_CO2, Reference_EF_Freight_CH4_NO2, Reference_EF_Road, Reference_EF_Fuel_Use_CH4_N2O, Reference_EF_Fuel_Use_CO2, Reference_Unit_Conversion
from Components.reference_lookups import ReferenceLookup
from Components.Reference_Source_Product_Matrix import Reference_Source_Product_Matrix
from Services.Co2FossilFuelCalculator import Co2FossilFuelCalculator
from config import get_config


# Get configuration
config = get_config()

# Initialize Flask app and CORS at the top
app = Flask(__name__)
CORS(app, origins=config.CORS_ORIGINS)

# Configure logging to reduce verbose output
if config.DEBUG:
    # Reduce werkzeug (Flask development server) logging level
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    # Set Flask app logger to WARNING level
    app.logger.setLevel(logging.WARNING)

# --- Reference - Lookups.csv Lookups ---
lookups_csv_path = config.get_csv_path('lookups')
lookup_columns = config.LOOKUP_COLUMNS
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
unit_conversion_csv_path = config.get_csv_path('unit_conversion')
reference_unit_conversion = Reference_Unit_Conversion(unit_conversion_csv_path)

# API endpoint for Reference_Unit_Conversion


@app.route('/api/unit_conversion', methods=['GET'])
def get_unit_conversion():
    from flask import request
    from_unit = request.args.get('from_unit', '')
    to_unit = request.args.get('to_unit', '')
    if not from_unit or not to_unit:
        return jsonify({'error': 'Both from_unit and to_unit query parameters are required'}), 400
    value = reference_unit_conversion.get_conversion(from_unit, to_unit)
    if value is None or value == '':
        return jsonify({'error': f'No conversion value found for from_unit: {from_unit}, to_unit: {to_unit}'}), 404
    return jsonify({'from_unit': from_unit, 'to_unit': to_unit, 'value': value})


# Initialize Reference_EF_Fuel_Use_CO2 instance (load once at startup)
ef_fuel_use_co2_csv_path = config.get_csv_path('ef_fuel_use_co2')
reference_ef_fuel_use_co2 = Reference_EF_Fuel_Use_CO2(ef_fuel_use_co2_csv_path)

# API endpoint for Reference_EF_Fuel_Use_CO2


@app.route('/api/ef_fuel_use_co2', methods=['GET'])
def get_ef_fuel_use_co2_by_fuel_and_region():
    from flask import request
    fuel = request.args.get('fuel', '')
    region = request.args.get('region', '')
    if not fuel or not region:
        return jsonify({'error': 'Both fuel and region query parameters are required'}), 400
    results = reference_ef_fuel_use_co2.get_by_fuel_and_region(fuel, region)
    if not results:
        return jsonify({'error': f'No data found for fuel: {fuel}, region: {region}'}), 404
    return jsonify({'results': results})


# Initialize Reference_EF_Fuel_Use_CH4_N2O instance (load once at startup)
ef_fuel_use_ch4_n2o_csv_path = config.get_csv_path('ef_fuel_use_ch4_n2o')
reference_ef_fuel_use_ch4_n2o = Reference_EF_Fuel_Use_CH4_N2O(
    ef_fuel_use_ch4_n2o_csv_path)

# API endpoint for Reference_EF_Fuel_Use_CH4_N2O


@app.route('/api/ef_fuel_use_ch4_n2o', methods=['GET'])
def get_ef_fuel_use_ch4_n2o_by_transport_and_region():
    from flask import request
    transport_and_fuel = request.args.get('transport_and_fuel', '')
    region = request.args.get('region', '')
    if not transport_and_fuel or not region:
        return jsonify({'error': 'Both transport_and_fuel and region query parameters are required'}), 400
    results = reference_ef_fuel_use_ch4_n2o.get_by_transport_and_region(
        transport_and_fuel, region)
    if not results:
        return jsonify({'error': f'No data found for transport_and_fuel: {transport_and_fuel}, region: {region}'}), 404
    return jsonify({'results': results})


# Initialize Reference_EF_Road instance (load once at startup)
ef_road_csv_path = config.get_csv_path('ef_road')
reference_ef_road = Reference_EF_Road(ef_road_csv_path)

# API endpoint for Reference_EF_Road


@app.route('/api/ef_road', methods=['GET'])
def get_ef_road_by_vehicle_and_region():
    from flask import request
    vehicle_fuel_year = request.args.get('vehicle_fuel_year', '')
    region = request.args.get('region', '')
    if not vehicle_fuel_year or not region:
        return jsonify({'error': 'Both vehicle_fuel_year and region query parameters are required'}), 400
    results = reference_ef_road.get_by_vehicle_and_region(
        vehicle_fuel_year, region)
    if not results:
        return jsonify({'error': f'No data found for vehicle_fuel_year: {vehicle_fuel_year}, region: {region}'}), 404
    return jsonify({'results': results})


# Initialize Reference_EF_Public instance (load once at startup)
ef_csv_path = config.get_csv_path('ef_public')
reference_ef = Reference_EF_Public(ef_csv_path)


# Initialize Reference_EF_Freight_CO2 instance (load once at startup)
ef_freight_csv_path = config.get_csv_path('ef_freight_co2')
reference_ef_freight = Reference_EF_Freight_CO2(ef_freight_csv_path)

# Initialize Reference_EF_Freight_CH4_NO2 instance (load once at startup)
ef_freight_ch4_no2_csv_path = config.get_csv_path('ef_freight_ch4_no2')
reference_ef_freight_ch4_no2 = Reference_EF_Freight_CH4_NO2(
    ef_freight_ch4_no2_csv_path)

# API endpoint for Reference_EF_Freight_CH4_NO2


@app.route('/api/ef_freight_ch4_no2', methods=['GET'])
def get_ef_freight_ch4_no2_by_vehicle_and_region():
    from flask import request
    vehicle_type = request.args.get('vehicle_type', '')
    region = request.args.get('region', '')
    if not vehicle_type or not region:
        return jsonify({'error': 'Both vehicle_type and region query parameters are required'}), 400
    results = reference_ef_freight_ch4_no2.get_by_vehicle_and_region(
        vehicle_type, region)
    if not results:
        return jsonify({'error': f'No data found for vehicle_type: {vehicle_type}, region: {region}'}), 404
    return jsonify({'results': results})

 # API endpoint for Reference_EF_Freight_CO2 (renamed to include co2)


@app.route('/api/ef_freight_co2', methods=['GET'])
def get_ef_freight_co2_by_vehicle_and_region():
    from flask import request
    vehicle_size = request.args.get('vehicle_size', '')
    region = request.args.get('region', '')
    if not vehicle_size or not region:
        return jsonify({'error': 'Both vehicle_size and region query parameters are required'}), 400
    results = reference_ef_freight.get_by_vehicle_and_region(
        vehicle_size, region)
    if not results:
        return jsonify({'error': f'No data found for vehicle_size: {vehicle_size}, region: {region}'}), 404
    return jsonify({'results': results})


@app.route('/api/ef', methods=['GET'])
def get_ef_by_vehicle_and_region():
    from flask import request
    vehicle_type = request.args.get('vehicle_type', '')
    region = request.args.get('region', '')
    if not vehicle_type or not region:
        return jsonify({'error': 'Both vehicle_type and region query parameters are required'}), 400
    results = reference_ef.get_by_vehicle_and_region(vehicle_type, region)
    if not results:
        return jsonify({'error': f'No data found for vehicle_type: {vehicle_type}, region: {region}'}), 404
    return jsonify({'results': results})


@app.route('/')
def home():
    return jsonify({'message': 'Avisk GHG Calculator Flask backend is running.'})


@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = []
    csv_path = config.get_csv_path('supplier_list')

    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            # Skip header row
            header = next(csv_reader)

            for row in csv_reader:
                if row:  # Check if row is not empty
                    # Remove quotes and trim whitespace
                    supplier = row[0].strip('"').strip()
                    suppliers.append(supplier)

        result = {'suppliers': suppliers}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- Load Reference_Source_Product_Matrix at startup ---
source_product_matrix_csv_path = config.get_csv_path('source_product_matrix')
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
    results = reference_source_product_matrix.filter_by_supplier_product_location(
        supplier_product_location)
    return jsonify({'results': results})


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
        return jsonify({'error': 'Failed to retrieve fuel types'}), 500


# --- API endpoint: compute_ghg_emissions ---
@app.route('/api/compute_ghg_emissions', methods=['POST'])
def compute_ghg_emissions():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing JSON body'}), 400

        # Extract supplier data
        supplier_data = data.get('supplier_data', {})
        activity_rows = data.get('activity_rows', [])

        # Process each activity row
        supplier_input_objects = []
        for i, row_data in enumerate(activity_rows):
            # Create Supplier_Input object for this row
            supplier_input = Supplier_Input(
                Supplier_and_Container=supplier_data.get(
                    'Supplier_and_Container', ''),
                Container_Weight=float(
                    supplier_data.get('Container_Weight', 0)),
                Number_Of_Containers=int(
                    supplier_data.get('Number_Of_Containers', 0)),
                Source_Description=row_data.get('Source_Description', ''),
                Region=row_data.get('Region', ''),
                Mode_of_Transport=row_data.get('Mode_of_Transport', ''),
                Scope=row_data.get('Scope', ''),
                Type_Of_Activity_Data=row_data.get(
                    'Type_Of_Activity_Data', ''),
                Vehicle_Type=row_data.get('Vehicle_Type'),
                Distance_Travelled=float(row_data['Distance_Travelled']) if row_data.get(
                    'Distance_Travelled') is not None else None,
                Total_Weight_Of_Freight_InTonne=float(row_data['Total_Weight_Of_Freight_InTonne']) if row_data.get(
                    'Total_Weight_Of_Freight_InTonne') is not None else None,
                Num_Of_Passenger=int(row_data['Num_Of_Passenger']) if row_data.get(
                    'Num_Of_Passenger') is not None else None,
                Units_of_Measurement=row_data.get('Units_of_Measurement'),
                Fuel_Used=row_data.get('Fuel_Used'),
                Fuel_Amount=float(row_data['Fuel_Amount']) if row_data.get(
                    'Fuel_Amount') is not None else None,
                Unit_Of_Fuel_Amount=row_data.get('Unit_Of_Fuel_Amount')
            )

            supplier_input_objects.append(supplier_input)

        # Calculate CO2 emissions using Co2FossilFuelCalculator with cached reference data
        co2_calculator = Co2FossilFuelCalculator(
            reference_ef_fuel_use_co2=reference_ef_fuel_use_co2,
            reference_ef_freight_co2=reference_ef_freight,
            reference_unit_conversion=reference_unit_conversion
        )

        co2_results = co2_calculator.calculate_co2_emissions(
            supplier_input_objects)

        # Create summarized data by Mode of Transport, Scope, Activity type, and GHG Type
        summary_data = {}

        # Initialize summary structure
        for i, row_data in enumerate(activity_rows):
            mode_of_transport = row_data.get('Mode_of_Transport', 'Unknown')
            scope = row_data.get('Scope', 'Unknown')
            activity_type = 'Fuel' if row_data.get(
                'Fuel_Used') and row_data.get('Fuel_Amount') else 'Distance'

            # Initialize nested structure if not exists
            if mode_of_transport not in summary_data:
                summary_data[mode_of_transport] = {}
            if scope not in summary_data[mode_of_transport]:
                summary_data[mode_of_transport][scope] = {}
            if activity_type not in summary_data[mode_of_transport][scope]:
                summary_data[mode_of_transport][scope][activity_type] = {}
            if 'CO2' not in summary_data[mode_of_transport][scope][activity_type]:
                summary_data[mode_of_transport][scope][activity_type]['CO2'] = {
                    'total_emissions': 0.0,
                    'details': []
                }

        # Aggregate the results into summary structure
        for i, result in enumerate(co2_results):
            if i < len(activity_rows):
                row_data = activity_rows[i]
                mode_of_transport = row_data.get(
                    'Mode_of_Transport', 'Unknown')
                scope = row_data.get('Scope', 'Unknown')
                activity_type = 'Fuel' if row_data.get(
                    'Fuel_Used') and row_data.get('Fuel_Amount') else 'Distance'

                # Add CO2 emissions to the appropriate category
                summary_data[mode_of_transport][scope][activity_type]['CO2']['total_emissions'] += result.get(
                    'co2_emissions', 0.0)

                # Add detailed information
                detail = {
                    'row_index': i,
                    'source_description': row_data.get('Source_Description', ''),
                    'vehicle_type': row_data.get('Vehicle_Type', ''),
                    'region': row_data.get('Region', ''),
                    'co2_emissions': result.get('co2_emissions', 0.0),
                    'emission_factor': result.get('emission_factor', 0.0),
                    'status': result.get('status', '')
                }

                if activity_type == 'Fuel':
                    detail.update({
                        'fuel_used': row_data.get('Fuel_Used', ''),
                        'fuel_amount': row_data.get('Fuel_Amount', 0),
                        'unit_of_fuel_amount': row_data.get('Unit_Of_Fuel_Amount', '')
                    })
                else:
                    detail.update({
                        'distance_travelled': row_data.get('Distance_Travelled', 0),
                        'total_weight_of_freight': row_data.get('Total_Weight_Of_Freight_InTonne', 0),
                        'units_of_measurement': row_data.get('Units_of_Measurement', '')
                    })

                summary_data[mode_of_transport][scope][activity_type]['CO2']['details'].append(
                    detail)

        # Calculate overall totals
        total_co2_emissions = sum(result['co2_emissions']
                                  for result in co2_results)

        # Manufacturing emissions calculation (from supplier data)
        container_weight = float(supplier_data.get('Container_Weight', 0))
        number_of_containers = int(
            supplier_data.get('Number_Of_Containers', 0))

        # Get supplier emission factor from Reference_Source_Product_Matrix
        supplier_and_container = supplier_data.get(
            'Supplier_and_Container', '')
        supplier_emission_factor = None

        if supplier_and_container:
            # Look up the emission factor using the Reference_Source_Product_Matrix
            supplier_emission_factor = reference_source_product_matrix.get_manufacturing_emissions_factor(
                supplier_and_container)

        # If no emission factor found in matrix, try to get from supplied data or use default
        if supplier_emission_factor is None:
            supplier_emission_factor = float(
                # Default fallback
                supplier_data.get('Supplier_Emission_Factor', 0.5))
            emission_factor_source = 'default/supplied'
        else:
            emission_factor_source = 'reference_matrix'

        manufacturing_emissions = (container_weight * number_of_containers *
                                   supplier_emission_factor) / 907184.74  # Convert to tonnes

        manufacturing_emissions_metric_tonnes = manufacturing_emissions * \
            (0.907185)  # Convert to Mertic tonnes

        # Return comprehensive results including summarized data
        return jsonify({
            'status': 'success',
            'supplier_data': supplier_data,
            'processed_rows': len(supplier_input_objects),
            'manufacturing_emissions': manufacturing_emissions,
            'manufacturing_details': {
                'supplier_emission_factor': supplier_emission_factor,
                'emission_factor_source': emission_factor_source,
                'container_weight': container_weight,
                'number_of_containers': number_of_containers,
                'total_material_weight_tonnes': (container_weight * number_of_containers) / 1000000,
                'manufacturing_emissions_metric_tonnes': manufacturing_emissions_metric_tonnes
            },
            'transport_emissions': {
                'co2': total_co2_emissions,
                'summary_by_transport_scope_activity': summary_data,
                'detailed_results': co2_results
            },
            'total_emissions': manufacturing_emissions_metric_tonnes + total_co2_emissions,
            'co2_emissions_results': co2_results,  # Keep for backward compatibility
            'total_co2_emissions': total_co2_emissions  # Keep for backward compatibility
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
