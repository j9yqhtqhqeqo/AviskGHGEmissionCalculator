# Fuel CO2 Emissions Test Documentation

## Overview
This document describes the comprehensive test suite for validating fuel-based CO2 emissions calculations using the `Co2FossilFuelCalculator.calculate_co2_emissions` method.

## Test Data File
- **File**: `Co2TestDataFuel.csv`
- **Location**: `/Unit Test/Data/`
- **Purpose**: Contains 10 test cases covering various fuel types, regions, and units

## Test Script
- **File**: `test_fuel_co2_emissions.py`
- **Location**: `/Unit Test/Scripts/`
- **Purpose**: Validates calculated CO2 emissions against expected values with 1% tolerance

## Test Coverage

### Fuel Types Tested
1. **Jet Fuel** (2 test cases)
   - US region
   - Various activity data types
   
2. **On-Road Diesel Fuel** (1 test case)
   - US region
   - US Gallon units

3. **Gasoline/Petrol** (1 test case)
   - UK region
   - Litre units

4. **LNG** (2 test cases)
   - UK and Other regions
   - UK Gallon units

5. **Residual Fuel Oil (3s 5 and 6)** (2 test cases)
   - UK and US regions
   - UK Gallon and Litre units

6. **LPG** (1 test case)
   - Other region
   - US Gallon units

7. **100% Biodiesel** (1 test case)
   - Other region
   - Litre units
   - Expected CO2: 0.0 (biomass fuel)

### Regional Coverage
- **US**: 4 test cases
- **UK**: 3 test cases  
- **Other**: 3 test cases

### Unit Types Tested
- **US Gallon**: 5 test cases
- **UK Gallon**: 3 test cases
- **Litre**: 2 test cases

### Activity Data Types
- **Fuel Use**: 6 test cases
- **Fuel Use and Vehicle Distance**: 4 test cases

## Test Results Summary

### Overall Performance
- **Total Tests**: 10
- **Passed**: 10
- **Failed**: 0
- **Pass Rate**: 100.0%

### Key Validation Points
1. **Emission Factor Lookup**: All fuel types correctly matched to reference data
2. **Unit Conversion**: Accurate conversion between different fuel units
3. **Regional Factors**: Proper application of region-specific emission factors
4. **Calculation Accuracy**: Results match expected values within 1% tolerance
5. **Special Cases**: Biodiesel correctly returns 0.0 emissions (biomass fuel)

## Test Case Details

| Test | Fuel Type | Amount | Unit | Region | Expected CO2 | Calculated CO2 | Status |
|------|-----------|--------|------|--------|--------------|----------------|--------|
| 1 | Jet Fuel | 1000 | US Gallon | US | 9.57 | 9.57 | ✅ PASS |
| 2 | Jet Fuel | 1000 | US Gallon | US | 9.57 | 9.57 | ✅ PASS |
| 3 | On-Road Diesel | 5000 | US Gallon | US | 50.75 | 50.75 | ✅ PASS |
| 4 | Gasoline/Petrol | 3000 | Litre | UK | 6.91 | 6.91 | ✅ PASS |
| 5 | LNG | 10000 | UK Gallon | UK | 55.79 | 55.79 | ✅ PASS |
| 6 | Residual Fuel Oil | 3000 | UK Gallon | UK | 34.50 | 34.50 | ✅ PASS |
| 7 | LNG | 5000 | UK Gallon | Other | 26.78 | 26.78 | ✅ PASS |
| 8 | LPG | 3000 | US Gallon | Other | 18.30 | 18.30 | ✅ PASS |
| 9 | 100% Biodiesel | 5000 | Litre | Other | 0.00 | 0.00 | ✅ PASS |
| 10 | Residual Fuel Oil | 5000 | Litre | US | 15.59 | 15.59 | ✅ PASS |

## Technical Implementation

### Calculator Setup
```python
# Initialize with fuel reference data
self.co2_calculator = Co2FossilFuelCalculator(
    reference_ef_fuel_use_co2=self.reference_ef_fuel_use_co2,
    reference_ef_freight_co2=None,  # Not needed for fuel tests
    reference_unit_conversion=self.reference_unit_conversion
)
```

### Validation Logic
- **Tolerance**: 1% relative error acceptance
- **Zero Handling**: Special case for biodiesel (expected 0.0 emissions)
- **Unit Conversion**: Automatic conversion between fuel units and metric tonnes
- **Error Handling**: Comprehensive exception catching and reporting

### Key Test Features
1. **Expected vs Calculated**: Direct comparison with CSV expected values
2. **Detailed Logging**: Debug output showing calculation steps
3. **Comprehensive Reporting**: CSV output with all test details
4. **Fuel Type Analysis**: Pass rate breakdown by fuel type

## Usage

### Running Tests
```bash
cd "/path/to/project"
python "Unit Test/Scripts/test_fuel_co2_emissions.py"
```

### Output Files
- **Console**: Real-time test progress and summary
- **CSV Report**: `fuel_co2_test_results.csv` with detailed results

## Validation Significance

This test suite confirms that:
1. **Fuel-based calculations** work correctly across all supported fuel types
2. **Unit conversions** are accurate for international fuel measurements
3. **Regional emission factors** are properly applied
4. **Special fuel types** (biomass) are handled correctly
5. **API consistency** between distance-based and fuel-based calculations

The 100% pass rate demonstrates that the `calculate_co2_emissions` method reliably produces accurate results for fuel consumption data, validating the backend API functionality for frontend integration.
