from .ammonia import Ammonia
from .biomass import Biomass
from .biomethane import Biomethane
from .carbon import Carbon
from .cement import Cement  # demandreductioncircularity
from .clinker import Clinker
from .clinker_input_material import ClinkerInputMaterial  # demandreductioncircularity
from .concrete import Concrete  # demandreductioncircularity
from .concrete_fine import ConcreteFine  # demandreductioncircularity
from .concrete_use import ConcreteUse  # demandreductioncircularity
from .concrete_waste import ConcreteWaste  # demandreductioncircularity
from .crude_oil import CrudeOil
from .diesel import Diesel
from .district_heat import DistrictHeat
from .electricity import Electricity
from .fuel_for_cement import FuelForCement
from .gasoline import Gasoline
from .hard_coal import HardCoal
from .heat import Heat
from .hydrogen import Hydrogen
from .kerosene import Kerosene
from .lignite import Lignite
from .lng import LNG
from .methanol import Methanol
from .naphtha import Naphtha
from .natural_gas import NaturalGas
from .oil import Oil
from .olefin import Olefin
from .passenger_mileage import PassengerMileage
from .primary_steel import PrimarySteel
from .raw_material_clinker import RawMaterialClinker  # demandreductioncircularity
from .scrap_steel import ScrapSteel  # demandreductioncircularity
from .secondary_steel import SecondarySteel
from .shipping import Shipping
from .steel import Steel  # demandreductioncircularity
from .truck_mileage import TruckMileage
from .uranium import Uranium
from .waste import Waste
from .wet_biomass import WetBiomass

__all__ = [
    "Biomass",
    "WetBiomass",
    "Electricity",
    "Ammonia",
    "Clinker",
    "Cement",  # demandreductioncircularity
    "Concrete",  # demandreductioncircularity
    "ConcreteUse",  # demandreductioncircularity
    "ConcreteWaste",  # demandreductioncircularity
    "ConcreteFine",  # demandreductioncircularity
    "RawMaterialClinker",  # demandreductioncircularity
    "ClinkerInputMaterial",  # demandreductioncircularity
    "Biomethane",
    "Hydrogen",
    "PrimarySteel",
    "SecondarySteel",
    "Steel",  # demandreductioncircularity
    "ScrapSteel",  # demandreductioncircularity
    "Carbon",
    "DistrictHeat",
    "Naphtha",
    "Methanol",
    "HardCoal",
    "Lignite",
    "Oil",
    "Waste",
    "Diesel",
    "Gasoline",
    "Olefin",
    "Kerosene",
    "Shipping",
    "LNG",
    "NaturalGas",
    "Heat",
    "PassengerMileage",
    "TruckMileage",
    "CrudeOil",
    "FuelForCement",
    "Uranium",
]
