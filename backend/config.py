import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the Flask backend application."""

    # Server configuration
    HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    PORT = int(os.getenv('FLASK_PORT', 5002))
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    # CORS configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

    # Data files configuration
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

    # CSV file paths
    CSV_FILES = {
        'lookups': 'Reference - Lookups.csv',
        'unit_conversion': 'Reference - Unit Conversion.csv',
        'ef_fuel_use_co2': 'Reference - EF Fuel Use CO2.csv',
        'ef_fuel_use_ch4_n2o': 'Reference - EF Fuel Use CH4 N2O.csv',
        'ef_road': 'Reference_EF_Road.csv',
        'ef_public': 'Reference_EF_Public.csv',
        'ef_freight_co2': 'Reference_EF_Freight_CO2.csv',
        'ef_freight_ch4_no2': 'Reference_EF_Freight_CH4_NO2.csv',
        'supplier_list': 'Supplier_List.csv',
        'source_product_matrix': 'Source_Product_Matrix.csv'
    }

    # Lookup columns configuration
    LOOKUP_COLUMNS = [
        'Region',
        'Mode of Transport',
        'Type of Activity Data',
        'Scope',
        'Units ',
        'IPCC GWP Version',
        'Activity Data Columns',
        'Unit of Fuel Amount'
    ]

    # API configuration
    API_PREFIX = '/api'

    @classmethod
    def get_csv_path(cls, csv_key: str) -> str:
        """Get the full path to a CSV file."""
        if csv_key not in cls.CSV_FILES:
            raise ValueError(f"Unknown CSV file key: {csv_key}")
        return os.path.join(cls.DATA_DIR, cls.CSV_FILES[csv_key])

    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """Get configuration as a dictionary."""
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'debug': cls.DEBUG,
            'cors_origins': cls.CORS_ORIGINS,
            'data_dir': cls.DATA_DIR,
            'api_prefix': cls.API_PREFIX
        }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5002


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = int(os.getenv('PORT', 5000))


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    HOST = '127.0.0.1'
    PORT = 5003


# Configuration mapping
config_map: Dict[str, type] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: str = 'development') -> Config:
    """Get configuration class based on environment."""
    if config_name is None:
        config_name = 'development'

    config_class = config_map.get(config_name, config_map['default'])
    return config_class()
