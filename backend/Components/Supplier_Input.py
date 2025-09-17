from dataclasses import dataclass
from typing import Optional


@dataclass
class Supplier_Input:
    Supplier_and_Container: str
    Container_Weight: float
    Number_Of_Containers: int
    Source_Description: str
    Region: str
    Mode_of_Transport: str
    Scope: str
    Type_Of_Activity_Data: str
    Selected_Type_Of_Activity_Data: Optional[str] = None
    Vehicle_Type: Optional[str] = None
    Distance_Travelled: Optional[float] = None
    Total_Weight_Of_Freight_InTonne: Optional[float] = None
    Num_Of_Passenger: Optional[int] = None
    Units_of_Measurement: Optional[str] = None
    Fuel_Used: Optional[str] = None
    Fuel_Amount: Optional[float] = None
    Unit_Of_Fuel_Amount: Optional[str] = None

    def __init__(self,
                 Supplier_and_Container: str,
                 Container_Weight: float,
                 Number_Of_Containers: int,
                 Source_Description: str,
                 Region: str,
                 Mode_of_Transport: str,
                 Scope: str,
                 Type_Of_Activity_Data: str,
                 Vehicle_Type: Optional[str] = None,
                 Distance_Travelled: Optional[float] = None,
                 Total_Weight_Of_Freight_InTonne: Optional[float] = None,
                 Num_Of_Passenger: Optional[int] = None,
                 Units_of_Measurement: Optional[str] = None,
                 Fuel_Used: Optional[str] = None,
                 Fuel_Amount: Optional[float] = None,
                 Unit_Of_Fuel_Amount: Optional[str] = None):
        self.Supplier_and_Container = Supplier_and_Container
        self.Container_Weight = Container_Weight
        self.Number_Of_Containers = Number_Of_Containers
        self.Source_Description = Source_Description
        self.Region = Region
        self.Mode_of_Transport = Mode_of_Transport
        self.Scope = Scope
        self.Type_Of_Activity_Data = Type_Of_Activity_Data
        self.Vehicle_Type = Vehicle_Type
        self.Distance_Travelled = Distance_Travelled
        self.Total_Weight_Of_Freight_InTonne = Total_Weight_Of_Freight_InTonne
        self.Num_Of_Passenger = Num_Of_Passenger
        self.Units_of_Measurement = Units_of_Measurement
        self.Fuel_Used = Fuel_Used
        self.Fuel_Amount = Fuel_Amount
        self.Unit_Of_Fuel_Amount = Unit_Of_Fuel_Amount
        # Compute Selected_Type_Of_Activity_Data using Excel logic
        if self.Type_Of_Activity_Data == "Custom vehicle":
            if self.Units_of_Measurement in ("Passenger Mile", "Passenger Kilometer"):
                self.Selected_Type_Of_Activity_Data = "Passenger Distance (e.g. Public Transport)"
            elif self.Units_of_Measurement in ("Tonne Mile", "Tonne Kilometer"):
                self.Selected_Type_Of_Activity_Data = "Weight Distance (e.g. Freight Transport)"
            else:
                self.Selected_Type_Of_Activity_Data = "Vehicle Distance (e.g. Road Transport)"
        else:
            self.Selected_Type_Of_Activity_Data = self.Type_Of_Activity_Data
