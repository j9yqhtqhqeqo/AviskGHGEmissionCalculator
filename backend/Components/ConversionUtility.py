
import os
import requests


class ConversionUtility:
    @classmethod
    def get_Co2_Factor(cls, fuel: str, region: str, type_of_activity_data: str = None, api_base_url: str = "http://127.0.0.1:5000") -> float:
        """
        Get CO2 emission factor for a specific fuel, region, and type of activity data using the API.

        Args:
            fuel (str): The fuel type to look up
            region (str): The region for the emission factor
            type_of_activity_data (str, optional): The type of activity data for additional filtering
            api_base_url (str, optional): The base URL for the API. Defaults to "http://localhost:5000".

        Returns:
            float: CO2 emission factor value
        """
        try:
            if type_of_activity_data in ("Fuel Use", "Fuel Use and Vehicle Distance"):
                return cls.get_CO2_Factor_By_Fuel_And_Region(fuel, region, api_base_url)
            # Placeholder for other logic if needed
            return 0.0
        except Exception as e:
            print(f"Error getting CO2 factor from API: {e}")
            return 0.0

    """
    Utility class for unit conversions and related helper methods.
    Add static methods for conversion logic as needed.
    """

    @classmethod
    def get_CO2_Factor_By_Fuel_And_Region(cls, fuel: str, region: str, api_base_url: str = "http://127.0.0.1:5000") -> float:
        """
        Get CO2 emission factor for a specific fuel and region using the API.

        Args:
            fuel (str): The fuel type to look up
            region (str): The region for the emission factor
            api_base_url (str, optional): The base URL for the API. Defaults to "http://localhost:5000".

        Returns:
            float: CO2 emission factor value
        """
        try:
            params = {"fuel": fuel, "region": region}
            response = requests.get(
                f"{api_base_url}/api/ef_fuel_use_co2", params=params)
            if response.status_code != 200:
                print(f"API error: {response.status_code} {response.text}")
                return 0.0
            data = response.json()
            results = data.get("results", [])
            if results:
                co2_value = results[0].get("CO2", "0.0")
                if co2_value and str(co2_value).strip():
                    return float(co2_value)
            return 0.0
        except Exception as e:
            print(f"Error getting CO2 factor from API: {e}")
            return 0.0


# Example usage
if __name__ == "__main__":
    # Test the get_CO2_Factor_By_Fuel_And_Region method with caching
    result = ConversionUtility.get_CO2_Factor_By_Fuel_And_Region(
        "Jet Fuel", "US")
    print(f"CO2 Factor for Jet Fuel in US region: {result}")
