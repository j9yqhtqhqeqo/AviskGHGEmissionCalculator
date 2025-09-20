class Co2FossilFuelCalculator:
    """
    Calculator for CO2 emissions from fossil fuel consumption.

    This class handles calculations for carbon dioxide emissions
    based on fossil fuel usage data.
    """

    def __init__(self, reference_ef_fuel_use_co2=None, reference_ef_freight_co2=None, reference_unit_conversion=None):
        """
        Initialize the Co2FossilFuelCalculator with reference data instances.

        Args:
            reference_ef_fuel_use_co2: Reference_EF_Fuel_Use_CO2 instance for fuel emission factors
            reference_ef_freight_co2: Reference_EF_Freight_CO2 instance for freight emission factors  
            reference_unit_conversion: Reference_Unit_Conversion instance for unit conversions
        """
        self.reference_ef_fuel_use_co2 = reference_ef_fuel_use_co2
        self.reference_ef_freight_co2 = reference_ef_freight_co2
        self.reference_unit_conversion = reference_unit_conversion

    def get_emission_factor_by_vehicle_and_region(self, vehicle_type, region=None, units_of_measurement='',):
        """
        Get the appropriate emission factor for the given vehicle type and region.

        Args:
            vehicle_type (str): Type of vehicle
            region (str, optional): Geographic region for regional factors

        Returns:
            float: Emission factor for the vehicle type and region
        """
        if not self.reference_ef_freight_co2 or not vehicle_type or not region:
            return 0.0

        try:
            # Use the cached freight reference data to get emission factor by vehicle and region
            results = self.reference_ef_freight_co2.get_by_vehicle_and_region(
                vehicle_type, region)

            if results and len(results) > 0:
                # Extract the CO2 emission factor and unit information from the first matching result
                result = results[0]

                # Extract CO2 unit numerator and denominator for additional calculations
                co2_unit_numerator = result.get('CO2 Unit - Numerator', '')
                co2_unit_denominator = result.get('CO2 Unit - Denominator', '')

                print(f"=== DEBUG: CO2 Emission Factor Calculation ===")
                print(f"Vehicle Type: {vehicle_type}")
                print(f"Region: {region}")
                print(f"Units of Measurement: {units_of_measurement}")
                print(f"CO2 Unit Numerator: {co2_unit_numerator}")
                print(f"CO2 Unit Denominator: {co2_unit_denominator}")

                # 1. CO2 in Factor Unit Conversion Numerator = Lookup using Reference_Unit_Conversion
                co2_factor_unit_conversion_numerator = 0.0
                if co2_unit_numerator and self.reference_unit_conversion:
                    try:
                        co2_factor_unit_conversion_numerator = self.reference_unit_conversion.get_conversion(
                            co2_unit_numerator, 'Metric Ton')
                        if co2_factor_unit_conversion_numerator is None or co2_factor_unit_conversion_numerator == '':
                            co2_factor_unit_conversion_numerator = 0.0
                        else:
                            # Convert string to float if conversion value is found
                            co2_factor_unit_conversion_numerator = float(
                                co2_factor_unit_conversion_numerator)
                    except (ValueError, TypeError, Exception):
                        # Handle cases where compound units (e.g., "Short Ton Mile", "Tonne Kilometer")
                        # are not available in the basic unit conversion matrix
                        co2_factor_unit_conversion_numerator = 0.0

                # 2. CO2 in Factor Unit Conversion Denominator = Lookup using Reference_Unit_Conversion
                co2_factor_unit_conversion_denominator = 0.0
                if units_of_measurement and co2_unit_denominator and self.reference_unit_conversion:
                    try:
                        co2_factor_unit_conversion_denominator = self.reference_unit_conversion.get_conversion(
                            units_of_measurement, co2_unit_denominator)
                        if co2_factor_unit_conversion_denominator is None or co2_factor_unit_conversion_denominator == '':
                            co2_factor_unit_conversion_denominator = 0.0
                        else:
                            # Convert string to float if conversion value is found
                            co2_factor_unit_conversion_denominator = float(
                                co2_factor_unit_conversion_denominator)
                    except (ValueError, TypeError, Exception):
                        # Handle cases where compound units are not available in the conversion matrix
                        co2_factor_unit_conversion_denominator = 0.0

                # 3. Calculate CO2 Emission Factor = emission_factor * numerator * denominator
                co2_emission_factor = 0.0

                # Try different possible column names for emission factor in freight data
                for col_name in ['CO2']:
                    if col_name in result and result[col_name]:
                        try:
                            emission_factor = float(result[col_name])
                            print(
                                f"Original Emission Factor ({col_name}): {emission_factor}")

                            # Calculate CO2 Emission Factor by multiplying all three components
                            co2_emission_factor = emission_factor * \
                                co2_factor_unit_conversion_numerator * co2_factor_unit_conversion_denominator

                            print(
                                f"Calculated CO2 Emission Factor: {co2_emission_factor}")
                            print(
                                f"Calculation: {emission_factor} × {co2_factor_unit_conversion_numerator} × {co2_factor_unit_conversion_denominator} = {co2_emission_factor}")
                            print(f"=== END DEBUG ===")

                            # Unit information is available for additional calculations within this method
                            # co2_unit_numerator and co2_unit_denominator can be used here
                            return co2_emission_factor
                        except (ValueError, TypeError):
                            continue

            return 0.0

        except Exception as e:
            # Handle lookup errors gracefully
            return 0.0

    def calculate_co2_emissions(self, supplier_inputs):
        """
        Calculate CO2 emissions for an array of supplier input objects.

        Args:
            supplier_inputs (list): Array of Supplier_Input objects containing fuel consumption data

        Returns:
            list: Array of CO2 emission results, each containing:
                - supplier_info: Supplier identification data
                - co2_emissions: Calculated CO2 emissions value
                - fuel_data: Original fuel consumption data used in calculation
                - emission_factor: Emission factor applied
        """
        results = []

        for supplier_input in supplier_inputs:
            try:
                # Extract vehicle and fuel-related data from supplier input
                fuel_used = getattr(supplier_input, 'Fuel_Used', None)
                fuel_amount = getattr(supplier_input, 'Fuel_Amount', None)
                vehicle_type = getattr(supplier_input, 'Vehicle_Type', None)
                region = getattr(supplier_input, 'Region', None)
                units_of_measurement = getattr(
                    supplier_input, 'Units_of_Measurement', '')
                distance_travelled = getattr(
                    supplier_input, 'Distance_Travelled', None)
                total_weight = getattr(
                    supplier_input, 'Total_Weight_Of_Freight_InTonne', None)

                # print(f"=== DEBUG: Processing supplier input ===")
                # print(f"Fuel Used: {fuel_used}")
                # print(f"Fuel Amount: {fuel_amount}")
                # print(f"Vehicle Type: {vehicle_type}")
                # print(f"Region: {region}")
                # print(f"Units of Measurement: {units_of_measurement}")

                # Get emission factor for the vehicle type and region (try even if no fuel data)
                emission_factor = 0.0
                co2_emissions = 0.0

                if vehicle_type and region:
                    emission_factor = self.get_emission_factor_by_vehicle_and_region(
                        vehicle_type, region, units_of_measurement)

                    # Calculate CO2 emissions = emission_factor * Distance_Travelled * Total_Weight_Of_Freight_InTonne

                    if distance_travelled is not None and total_weight is not None and emission_factor > 0:
                        co2_emissions = emission_factor * \
                            float(distance_travelled) * float(total_weight)
                        print(f"CO2 Emissions: {co2_emissions}")
                    else:
                        co2_emissions = 0.0
                        print(f"CO2 Emissions: {co2_emissions}")

                else:
                    pass

                # Skip calculation if no fuel data available, but still record the emission factor attempt
                if not fuel_used or fuel_amount is None:
                    results.append({
                        'supplier_info': {
                            'supplier_container': getattr(supplier_input, 'Supplier_and_Container', ''),
                            'source_description': getattr(supplier_input, 'Source_Description', '')
                        },
                        'co2_emissions': 0.0,
                        'fuel_data': {
                            'fuel_used': fuel_used,
                            'fuel_amount': fuel_amount,
                            'unit': getattr(supplier_input, 'Unit_Of_Fuel_Amount', '')
                        },
                        'emission_factor': emission_factor,
                        'status': 'No fuel data available'
                    })
                    continue

                # # Calculate CO2 emissions
                # co2_emissions = self.calculate_emissions(
                #     fuel_amount, fuel_used, emission_factor)

                # Add result to results array
                results.append({
                    'supplier_info': {
                        'supplier_container': getattr(supplier_input, 'Supplier_and_Container', ''),
                        'source_description': getattr(supplier_input, 'Source_Description', '')
                    },
                    'co2_emissions': co2_emissions if co2_emissions is not None else 0.0,
                    'fuel_data': {
                        'fuel_used': fuel_used,
                        'fuel_amount': fuel_amount,
                        'unit': getattr(supplier_input, 'Unit_Of_Fuel_Amount', '')
                    },
                    'emission_factor': emission_factor if emission_factor is not None else 0.0,
                    'status': 'Success'
                })

            except Exception as e:
                # Handle calculation errors gracefully
                results.append({
                    'supplier_info': {
                        'supplier_container': getattr(supplier_input, 'Supplier_and_Container', ''),
                        'source_description': getattr(supplier_input, 'Source_Description', '')
                    },
                    'co2_emissions': 0.0,
                    'fuel_data': {
                        'fuel_used': getattr(supplier_input, 'Fuel_Used', None),
                        'fuel_amount': getattr(supplier_input, 'Fuel_Amount', None),
                        'unit': getattr(supplier_input, 'Unit_Of_Fuel_Amount', '')
                    },
                    'emission_factor': 0.0,
                    'status': f'Calculation error: {str(e)}'
                })

        return results
