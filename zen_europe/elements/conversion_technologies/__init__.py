from .ammonia_ICE_ship import AmmoniaICEShip
from .anaerobic_digestion import AnaerobicDigestion
from .BEV import BEV
from .BF_BOF import BF_BOF
from .biomass_boiler import BiomassBoiler
from .biomass_boiler_DH import BiomassBoilerDH
from .biomass_plant import BiomassPlant
from .biomethane_conversion import BiomethaneConversion
from .bus_BEV import Bus_BEV  # demandreductioncircularity
from .bus_ICE_diesel import Bus_ICE_diesel  # demandreductioncircularity
from .bus_to_urban import BusToUrban  # demandreductioncircularity
from .car_passenger_mileage_to_regional import (  # demandreductioncircularity
    CarPassengerMileageToRegional,
)
from .car_passenger_mileage_to_urban import (  # demandreductioncircularity
    CarPassengerMileageToUrban,
)
from .carbon_storage import CarbonStorage
from .cement_fines_for_clinker import (
    CementFinesForClinker,  # demandreductioncircularity
)
from .cement_kiln import CementKiln
from .cement_recycling import CementRecycling  # demandreductioncircularity
from .cement_to_concrete import CementToConcrete  # demandreductioncircularity
from .chemical_recycling_plastic import (
    ChemicalRecyclingPlastic,  # demandreductioncircularity
)
from .clinker_to_cement import ClinkerToCement  # demandreductioncircularity
from .concrete_demolishment_overproduction import (
    ConcreteDemolishmentOverproduction,  # demandreductioncircularity
)
from .concrete_fine_collection import (
    ConcreteFineCollection,  # demandreductioncircularity
)
from .DAC import DAC
from .diesel_ICE_ship import DieselICEShip
from .district_heating_grid import DistrictHeatingGrid
from .EAF import EAF
from .electrode_boiler import ElectrodeBoiler
from .electrode_boiler_DH import ElectrodeBoilerDH
from .electrolysis import Electrolysis
from .fischer_tropsch import FischerTropsch
from .fuel_cell import FuelCell
from .gasification import Gasification
from .H2_DRI import H2_DRI
from .haber_bosch import HaberBosch
from .hard_coal_boiler_DH import HardCoalBoilerDH
from .hard_coal_plant import HardCoalPlant
from .HDT_BET import HDT_BET
from .HDT_diesel import HDT_diesel
from .HDT_FCEV import HDT_FCEV
from .heat_pump import HeatPump
from .heat_pump_DH import HeatPumpDH
from .hydrogen_FC_ship import HydrogenFCShip
from .ICE_diesel import ICE_diesel
from .ICE_petrol import ICE_petrol
from .incineration_plastic import IncinerationPlastic  # demandreductioncircularity
from .lignite_coal_plant import LigniteCoalPlant
from .lng_terminal import LNGTerminal
from .mechanical_recycling_plastic import (
    MechanicalRecyclingPlastic,  # demandreductioncircularity
)
from .methanation import Methanation
from .methanol_from_biomass import MethanolFromBiomass
from .methanol_from_hydrogen import MethanolFromHydrogen
from .methanol_from_natural_gas import MethanolFromNaturalGas
from .methanol_ICE_ship import MethanolICEShip
from .natural_gas_boiler import NaturalGasBoiler
from .natural_gas_boiler_DH import NaturalGasBoilerDH
from .natural_gas_turbine import NaturalGasTurbine
from .NG_DRI import NG_DRI
from .nuclear import Nuclear
from .oil_boiler import OilBoiler
from .oil_boiler_DH import OilBoilerDH
from .oil_plant import OilPlant
from .oil_to_diesel_conversion import OilToDieselConversion
from .oil_to_gasoline_conversion import OilToGasolineConversion
from .oil_to_kerosene_conversion import OilToKeroseneConversion
from .oil_to_naphtha_conversion import OilToNaphthaConversion
from .olefin_from_methanol import OlefinFromMethanol
from .olefin_from_naphtha import OlefinFromNaphtha
from .olefins_to_nonplastics import (
    OlefinsToNonplastics,  # demandreductioncircularity
)
from .overproduction_use_plastic import (
    OverproductionUsePlastic,  # demandreductioncircularity
)
from .photovoltaics import Photovoltaics
from .polymerisation import Polymerisation  # demandreductioncircularity
from .primary_steel_to_steel import PrimarySteelToSteel  # demandreductioncircularity
from .pyrolysis import Pyrolysis
from .raw_material_for_clinker import (
    RawMaterialForClinker,  # demandreductioncircularity
)
from .refining import Refining
from .run_of_river_hydro import RunOfRiverHydro
from .secondary_steel_to_steel import (
 SecondarySteelToSteel,  # demandreductioncircularity
)
from .SMR import SMR
from .train import Train  # demandreductioncircularity
from .train_passenger_mileage_to_regional import (  # demandreductioncircularity
    TrainPassengerMileageToRegional,
)
from .tram_metro import TramMetro  # demandreductioncircularity
from .tram_metro_to_urban import TramMetroToUrban  # demandreductioncircularity
from .waste_boiler_DH import WasteBoilerDH
from .waste_plant import WastePlant
from .wind_offshore import WindOffshore
from .wind_onshore import WindOnshore

__all__ = [
    "Photovoltaics",
    "DistrictHeatingGrid",
    "WindOffshore",
    "WindOnshore",
    "RunOfRiverHydro",
    "HardCoalPlant",
    "LigniteCoalPlant",
    "NaturalGasTurbine",
    "Nuclear",
    "OilPlant",
    "BiomassPlant",
    "WastePlant",
    "NaturalGasBoiler",
    "HeatPump",
    "OilBoiler",
    "BiomassBoiler",
    "ElectrodeBoiler",
    "NaturalGasBoilerDH",
    "HardCoalBoilerDH",
    "OilBoilerDH",
    "BiomassBoilerDH",
    "ElectrodeBoilerDH",
    "WasteBoilerDH",
    "HeatPumpDH",
    "LNGTerminal",
    "CarbonStorage",
    "SMR",
    "Electrolysis",
    "Gasification",
    "FischerTropsch",
    "Methanation",
    "AnaerobicDigestion",
    "BiomethaneConversion",
    "FuelCell",
    "DAC",
    "Refining",
    "MethanolFromNaturalGas",
    "MethanolFromBiomass",
    "MethanolFromHydrogen",
    "OlefinFromMethanol",
    "OlefinFromNaphtha",
    "Polymerisation",  # demandreductioncircularity
    "OverproductionUsePlastic",  # demandreductioncircularity
    "MechanicalRecyclingPlastic",  # demandreductioncircularity
    "ChemicalRecyclingPlastic",  # demandreductioncircularity
    "IncinerationPlastic",  # demandreductioncircularity
    "OlefinsToNonplastics",  # demandreductioncircularity
    "HaberBosch",
    "CementKiln",
    "ClinkerToCement",  # demandreductioncircularity
    "CementToConcrete",  # demandreductioncircularity
    "ConcreteDemolishmentOverproduction",  # demandreductioncircularity
    "ConcreteFineCollection",  # demandreductioncircularity
    "CementRecycling",  # demandreductioncircularity
    "RawMaterialForClinker",  # demandreductioncircularity
    "CementFinesForClinker",  # demandreductioncircularity
    "BF_BOF",
    "H2_DRI",
    "NG_DRI",
    "EAF",
    "PrimarySteelToSteel",  # demandreductioncircularity
    "SecondarySteelToSteel",  # demandreductioncircularity
    "Pyrolysis",
    "DieselICEShip",
    "HydrogenFCShip",
    "MethanolICEShip",
    "AmmoniaICEShip",
    "OilToGasolineConversion",
    "OilToDieselConversion",
    "OilToNaphthaConversion",
    "OilToKeroseneConversion",
    "BEV",
    "ICE_diesel",
    "ICE_petrol",
    # demandreductioncircularity: passenger transport chain
    "Bus_ICE_diesel",
    "Bus_BEV",
    "TramMetro",
    "Train",
    "CarPassengerMileageToUrban",
    "CarPassengerMileageToRegional",
    "BusToUrban",
    "TramMetroToUrban",
    "TrainPassengerMileageToRegional",
    "HDT_diesel",
    "HDT_BET",
    "HDT_FCEV",
]
