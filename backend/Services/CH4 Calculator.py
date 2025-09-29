class Ch4Calculator:
    """
    Calculator for CH4 emissions from fuel consumption and freight transport.

    This class handles calculations for methane emissions
    based on fuel usage data and freight transport data.
    """

    def __init__(self, reference_ef_fuel_use_ch4_n2o=None, reference_ef_freight_co2=None, reference_unit_conversion=None):
        """
        Initialize the Ch4Calculator with reference data instances.

        Args:
            reference_ef_fuel_use_ch4_n2o: Reference_EF_Fuel_Use_CH4_N2O instance for fuel emission factors
            reference_ef_freight_co2: Reference_EF_Freight_CO2 instance for freight emission factors (contains CH4 data)
            reference_unit_conversion: Reference_Unit_Conversion instance for unit conversions
        """
        self.reference_ef_fuel_use_ch4_n2o = reference_ef_fuel_use_ch4_n2o
        self.reference_ef_freight_co2 = reference_ef_freight_co2
        self.reference_unit_conversion = reference_unit_conversion

    def get_emission_factor_by_vehicle_and_region(self, vehicle_type, region=None, units_of_measurement=''):
        """
        Get the appropriate CH4 emission factor for the given vehicle type and region.

        Args:
            vehicle_type (str): Type of vehicle
            region (str, optional): Geographic region for regional factors
            units_of_measurement (str): Units of measurement for the calculation

        Returns:
            float: CH4 emission factor for the vehicle type and region
        """
        if not self.reference_ef_freight_co2 or not vehicle_type or not region:
            return 0.0

        try:
            # Use the cached freight CO2 reference data to get emission factor by vehicle and region
            results = self.reference_ef_freight_co2.get_by_vehicle_and_region(
                vehicle_type, region)

            if results and len(results) > 0:
                # Extract the CH4 emission factor and unit information from the first matching result
                result = results[0]

                # Extract CH4 unit numerator and denominator for additional calculations
                ch4_unit_numerator = result.get('CH4 Unit - Numerator', '')
                ch4_unit_denominator = result.get('CH4 Unit - Denominator', '')

                print(f"=== DEBUG: CH4 Emission Factor Calculation ===")
                print(f"Vehicle Type: {vehicle_type}")
                print(f"Region: {region}")
                print(f"Units of Measurement: {units_of_measurement}")
                print(f"CH4 Unit Numerator: {ch4_unit_numerator}")
                print(f"CH4 Unit Denominator: {ch4_unit_denominator}")

                # 1. CH4 in Factor Unit Conversion Numerator = Lookup using Reference_Unit_Conversion
                ch4_factor_unit_conversion_numerator = 0.0
                if ch4_unit_numerator and self.reference_unit_conversion:
                    try:
                        ch4_factor_unit_conversion_numerator = self.reference_unit_conversion.get_conversion(
                            ch4_unit_numerator, 'Metric Ton')
                        if ch4_factor_unit_conversion_numerator is None or ch4_factor_unit_conversion_numerator == '':
                            ch4_factor_unit_conversion_numerator = 0.0
                        else:
                            # Convert string to float if conversion value is found
                            ch4_factor_unit_conversion_numerator = float(
                                ch4_factor_unit_conversion_numerator)
                    except (ValueError, TypeError, Exception):
                        # Handle cases where compound units (e.g., "Short Ton Mile", "Tonne Kilometer")
                        # are not available in the basic unit conversion matrix
                        ch4_factor_unit_conversion_numerator = 0.0

                # 2. CH4 in Factor Unit Conversion Denominator = Lookup using Reference_Unit_Conversion
                ch4_factor_unit_conversion_denominator = 0.0
                if units_of_measurement and ch4_unit_denominator and self.reference_unit_conversion:
                    try:
                        ch4_factor_unit_conversion_denominator = self.reference_unit_conversion.get_conversion(
                            units_of_measurement, ch4_unit_denominator)
                        if ch4_factor_unit_conversion_denominator is None or ch4_factor_unit_conversion_denominator == '':
                            ch4_factor_unit_conversion_denominator = 0.0
                        else:
                            # Convert string to float if conversion value is found
                            ch4_factor_unit_conversion_denominator = float(
                                ch4_factor_unit_conversion_denominator)
                    except (ValueError, TypeError, Exception):
                        # Handle cases where compound units are not available in the conversion matrix
                        ch4_factor_unit_conversion_denominator = 0.0

                # 3. Calculate CH4 Emission Factor = emission_factor * numerator * denominator
                ch4_emission_factor = 0.0

                # Try different possible column names for emission factor in freight data
                for col_name in ['CH4']:
                    if col_name in result and result[col_name]:
                        try:
                            emission_factor = float(result[col_name])
                            print(
                                f"Original Emission Factor ({col_name}): {emission_factor}")

                            # Calculate CH4 Emission Factor by multiplying all three components
                            ch4_emission_factor = emission_factor * \
                                ch4_factor_unit_conversion_numerator * ch4_factor_unit_conversion_denominator

                            print(
                                f"Calculated CH4 Emission Factor: {ch4_emission_factor}")
                            print(
                                f"Calculation: {emission_factor} × {ch4_factor_unit_conversion_numerator} × {ch4_factor_unit_conversion_denominator} = {ch4_emission_factor}")
                            print(f"=== END DEBUG ===")

                            # Unit information is available for additional calculations within this method
                            # ch4_unit_numerator and ch4_unit_denominator can be used here
                            return ch4_emission_factor
                        except (ValueError, TypeError):
                            continue

            return 0.0

        except Exception as e:
            # Handle lookup errors gracefully
            print(
                f"Error in get_emission_factor_by_vehicle_and_region: {str(e)}")
            return 0.0

    def get_emission_factor_by_fuel_consumption(self, fuel_used, fuel_amount, unit_of_fuel_amount, region=None):
        """
        Get the appropriate CH4 emission factor for the given fuel consumption data.

        Args:
            fuel_used (str): Type of fuel used (e.g., "Diesel", "Petrol", "Natural Gas")
            fuel_amount (float): Amount of fuel consumed
            unit_of_fuel_amount (str): Unit of measurement for fuel amount (e.g., "Litres", "Gallons", "m3")
            region (str, optional): Geographic region for regional factors

        Returns:
            float: CH4 emission factor for the fuel consumption
        """
        if not self.reference_ef_fuel_use_ch4_n2o or not fuel_used or fuel_amount is None:
            return 0.0

        try:
            # Use the cached fuel use reference data to get emission factor by fuel and region
            results = self.reference_ef_fuel_use_ch4_n2o.get_by_transport_and_region(
                fuel_used, region)

            if results and len(results) > 0:
                # Extract the CH4 emission factor and unit information from the first matching result
                result = results[0]

                # Extract CH4 unit numerator and denominator for additional calculations
                ch4_unit_numerator = result.get('CH4 Unit - Numerator', '')
                ch4_unit_denominator = result.get('CH4 Unit - Denominator', '')

                print(f"=== DEBUG: Fuel CH4 Emission Factor Calculation ===")
                print(f"Fuel Used: {fuel_used}")
                print(f"Fuel Amount: {fuel_amount}")
                print(f"Unit of Fuel Amount: {unit_of_fuel_amount}")
                print(f"Region: {region}")
                print(f"CH4 Unit Numerator: {ch4_unit_numerator}")
                print(f"CH4 Unit Denominator: {ch4_unit_denominator}")

                # 1. CH4 in Factor Unit Conversion Numerator = Lookup using Reference_Unit_Conversion
                ch4_factor_unit_conversion_numerator = 0.0
                if ch4_unit_numerator and self.reference_unit_conversion:
                    try:
                        ch4_factor_unit_conversion_numerator = self.reference_unit_conversion.get_conversion(
                            ch4_unit_numerator, 'Metric Ton')
                        if ch4_factor_unit_conversion_numerator is None or ch4_factor_unit_conversion_numerator == '':
                            ch4_factor_unit_conversion_numerator = 0.0
                        else:
                            # Convert string to float if conversion value is found
                            ch4_factor_unit_conversion_numerator = float(
                                ch4_factor_unit_conversion_numerator)
                    except (ValueError, TypeError, Exception):
                        # Handle cases where compound units are not available in the basic unit conversion matrix
                        ch4_factor_unit_conversion_numerator = 0.0

                # 2. CH4 in Factor Unit Conversion Denominator = Lookup using Reference_Unit_Conversion
                ch4_factor_unit_conversion_denominator = 0.0
                if unit_of_fuel_amount and ch4_unit_denominator and self.reference_unit_conversion:
                    try:
                        ch4_factor_unit_conversion_denominator = self.reference_unit_conversion.get_conversion(
                            unit_of_fuel_amount, ch4_unit_denominator)
                        if ch4_factor_unit_conversion_denominator is None or ch4_factor_unit_conversion_denominator == '':
                            ch4_factor_unit_conversion_denominator = 0.0
                        else:
                            # Convert string to float if conversion value is found
                            ch4_factor_unit_conversion_denominator = float(
                                ch4_factor_unit_conversion_denominator)
                    except (ValueError, TypeError, Exception):
                        # Handle cases where compound units are not available in the conversion matrix
                        ch4_factor_unit_conversion_denominator = 0.0

                # 3. Calculate CH4 Emission Factor = emission_factor * numerator * denominator
                ch4_emission_factor = 0.0

                # Try different possible column names for emission factor in fuel data
                for col_name in ['CH4']:
                    if col_name in result and result[col_name]:
                        try:
                            emission_factor = float(result[col_name])
                            print(
                                f"Original Fuel Emission Factor ({col_name}): {emission_factor}")

                            # Calculate CH4 Emission Factor by multiplying all three components
                            ch4_emission_factor = emission_factor * \
                                ch4_factor_unit_conversion_numerator * ch4_factor_unit_conversion_denominator

                            print(
                                f"Calculated Fuel CH4 Emission Factor: {ch4_emission_factor}")
                            print(
                                f"Calculation: {emission_factor} × {ch4_factor_unit_conversion_numerator} × {ch4_factor_unit_conversion_denominator} = {ch4_emission_factor}")
                            print(f"=== END DEBUG ===")

                            return ch4_emission_factor
                        except (ValueError, TypeError):
                            continue

            return 0.0

        except Exception as e:
            # Handle lookup errors gracefully
            print(
                f"Error in get_emission_factor_by_fuel_consumption: {str(e)}")
            return 0.0

    def calculate_ch4_emissions(self, supplier_inputs):
        """
        Calculate CH4 emissions for an array of supplier input objects.

        Args:
            supplier_inputs (list): Array of Supplier_Input objects containing fuel consumption data

        Returns:
            list: Array of CH4 emission results, each containing:
                - supplier_info: Supplier identification data
                - ch4_emissions: Calculated CH4 emissions value
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

                # Get emission factor for the vehicle type and region (try even if no fuel data)
                emission_factor = 0.0
                ch4_emissions = 0.0

                # Try fuel-based calculation first if fuel data is available
                if fuel_used and fuel_amount is not None:
                    unit_of_fuel_amount = getattr(
                        supplier_input, 'Unit_Of_Fuel_Amount', '')
                    fuel_emission_factor = self.get_emission_factor_by_fuel_consumption(
                        fuel_used, fuel_amount, unit_of_fuel_amount, region)

                    if fuel_emission_factor > 0:
                        # Calculate CH4 emissions = fuel_emission_factor * fuel_amount
                        ch4_emissions = fuel_emission_factor * \
                            float(fuel_amount)
                        emission_factor = fuel_emission_factor
                        print(f"Fuel-based CH4 Emissions: {ch4_emissions}")
                    else:
                        print(
                            f"Fuel-based CH4 Emissions: 0.0 (no fuel emission factor found)")

                # If no fuel data or fuel-based calculation failed, try vehicle/distance-based calculation
                elif vehicle_type and region:
                    emission_factor = self.get_emission_factor_by_vehicle_and_region(
                        vehicle_type, region, units_of_measurement)

                    # Calculate CH4 emissions = emission_factor * Distance_Travelled * Total_Weight_Of_Freight_InTonne
                    if distance_travelled is not None and total_weight is not None and emission_factor > 0:
                        ch4_emissions = emission_factor * \
                            float(distance_travelled) * float(total_weight)
                        print(
                            f"Distance/Weight-based CH4 Emissions: {ch4_emissions}")
                    else:
                        ch4_emissions = 0.0
                        print(
                            f"Distance/Weight-based CH4 Emissions: {ch4_emissions}")

                else:
                    print(f"CH4 Emissions: 0.0 (insufficient data for calculation)")

                # Add result to results array (regardless of fuel data availability)
                results.append({
                    'supplier_info': {
                        'supplier_container': getattr(supplier_input, 'Supplier_and_Container', ''),
                        'source_description': getattr(supplier_input, 'Source_Description', '')
                    },
                    'ch4_emissions': ch4_emissions if ch4_emissions is not None else 0.0,
                    'fuel_data': {
                        'fuel_used': fuel_used,
                        'fuel_amount': fuel_amount,
                        'unit': getattr(supplier_input, 'Unit_Of_Fuel_Amount', '')
                    },
                    'emission_factor': emission_factor if emission_factor is not None else 0.0,
                    'status': 'Success' if ch4_emissions > 0 else 'No emissions calculated'
                })

            except Exception as e:
                # Handle calculation errors gracefully
                results.append({
                    'supplier_info': {
                        'supplier_container': getattr(supplier_input, 'Supplier_and_Container', ''),
                        'source_description': getattr(supplier_input, 'Source_Description', '')
                    },
                    'ch4_emissions': 0.0,
                    'fuel_data': {
                        'fuel_used': getattr(supplier_input, 'Fuel_Used', None),
                        'fuel_amount': getattr(supplier_input, 'Fuel_Amount', None),
                        'unit': getattr(supplier_input, 'Unit_Of_Fuel_Amount', '')
                    },
                    'emission_factor': 0.0,
                    'status': f'Calculation error: {str(e)}'
                })

        return results
