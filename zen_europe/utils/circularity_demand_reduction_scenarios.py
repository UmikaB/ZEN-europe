# demandreductioncircularity: new file, scenarios of the MSc thesis of U. Bhagole
"""Scenarios for demand reduction and circularity strategies.

The five scenarios of the MSc thesis of U. Bhagole.
Each scenario is applied on top of the reference by changing a few
attributes.

The factors are listed per carrier or technology below and are used by the
elements, see e.g. ``elements/carriers/steel.py``.
"""

from zen_creator import Scenario

# scenario names
COMPACT_CITIES = "compact_cities"
INDUSTRIAL_CIRCULAR_PUSH = "industrial_circular_push"
EFFICIENCY_IMPROVEMENTS = "efficiency_improvements"
CONSUMER_DEMAND_REDUCTION = "consumer_demand_reduction"
CRISIS = "crisis"

# factors on the final demand of a carrier, per scenario
DEMAND_FACTORS: dict[str, dict[str, float]] = {
    "steel": {
        # material efficiency: -10% (Material Economics 2019 )
        INDUSTRIAL_CIRCULAR_PUSH: 0.90,
        # longer lifetimes, repair and reuse: -5% ([110], worldsteel 2023 )
        CONSUMER_DEMAND_REDUCTION: 0.95,
        # reduced steel output: -25% )
        CRISIS: 0.75,
    },
    # demandreductioncircularity: cement and concrete chain
    "concrete_use": {
        # optimised design, less concrete per structure: -35% (Material
        # Economics 2019 [110])
        INDUSTRIAL_CIRCULAR_PUSH: 0.65,
        # reduced cement and concrete output: -16% (ING 2023 [146], ZKG 2023 [147])
        CRISIS: 0.84,
    },
    # demandreductioncircularity: plastics chain
    "plastic_use": {
        # design for function, less overuse and overspecification in packaging:
        # -5% (Material Economics 2019 [110])
        INDUSTRIAL_CIRCULAR_PUSH: 0.95,
        # less packaging, reuse and sharing: -15% (Material Economics 2019 [110],
        # JRC 2022 [139])
        CONSUMER_DEMAND_REDUCTION: 0.85,
        # reduced plastic output: -8% (Financial Times 2024 [148]); in the thesis
        # table but not in the thesis runs, added here (see the Excel overview)
        CRISIS: 0.92,
    },
    # demandreductioncircularity: passenger transport chain
    "urban_transport": {
        # compact city design, more walking and cycling: -11% (Mason et al. [108])
        COMPACT_CITIES: 0.89,
        # remote work, trip avoidance, limited modal shift: -10% (EEA 2022 [135],
        # Walsh et al. [136])
        CONSUMER_DEMAND_REDUCTION: 0.90,
        # lockdowns and travel restrictions, 2020 vs 2019: -21.6% (EU Statistical
        # Pocketbook [59], ERF 2023 [142])
        CRISIS: 0.784,
    },
    "regional_transport": {
        # fewer commutes and business trips: -10% (EEA 2022 [135], ICCT [137])
        CONSUMER_DEMAND_REDUCTION: 0.90,
        # lockdowns and travel restrictions, 2020 vs 2019: -23.6% ([59], [142])
        CRISIS: 0.764,
    },
# demandreductioncircularity: other final demands
    "kerosene": {
        # aircraft efficiency, aviation not modelled explicitly: -19.6% (IEA Net
        # Zero by 2050)
        EFFICIENCY_IMPROVEMENTS: 0.804,
        # fewer flights, rail substitution: -15% (IEA)
        CONSUMER_DEMAND_REDUCTION: 0.85,
        # lockdowns and travel restrictions, 2020 vs 2019: -55%
        CRISIS: 0.45,
    },
    "shipping": {
        # less shipping during the lockdowns: -11%
        CRISIS: 0.89,
    },
    "heat": {
        # thermostat setback, boiler tuning, shorter showers: -15%
        CONSUMER_DEMAND_REDUCTION: 0.85,
        # behavioural heat conservation during the energy crisis: -10% =
        CRISIS: 0.90,
    },
    "electricity": {
        # LEDs, efficient appliances, standby cuts: -20% ;
        CONSUMER_DEMAND_REDUCTION: 0.80,
        # behavioural electricity conservation during the energy crisis: -10%
        CRISIS: 0.90,
    },
}

# industrial circular push: scrap steel availability from the upper-bound JRC
# projection (secondary steel ~70% above 2018, ~77% share in 2050) instead of
# the lower bound (JRC 2021 )
SCRAP_STEEL_AVAILABILITY_FACTOR = 1.29

# efficiency improvements: EAF process efficiency, -15% electricity per tonne
# of crude steel (Material Economics 2019 )
EAF_ELECTRICITY_FACTOR = 0.85

# demandreductioncircularity: efficiency improvements in the cement chain
# (Material Economics 2019)
# kiln energy -10%: fuel for cement and electricity of cement_kiln
CEMENT_KILN_ENERGY_FACTOR = 0.90
# clinker-to-cement ratio from 0.70 to 0.50 (-28.6%): clinker of clinker_to_cement
CLINKER_TO_CEMENT_CLINKER_FACTOR = 0.50 / 0.70
# raw meal preparation -15%: raw material of raw_material_for_clinker
RAW_MATERIAL_FOR_CLINKER_FACTOR = 0.85
# demandreductioncircularity: efficiency improvements in polymerisation, process
# efficiency +15% (Material Economics 2019 ): electricity and heat of
# polymerisation x0.85. Olefin stays 1 t/t to keep the mass balance
POLYMERISATION_ENERGY_FACTOR = 0.85

# demandreductioncircularity: passenger transport chain
# compact cities: the share of urban car travel is set to 50% of each country's
# 2019 share, as minimum and maximum (
COMPACT_CITIES_CAR_SHARE_FACTOR = 0.5
# efficiency improvements: factor on the energy input per passenger-km
TRANSPORT_EFFICIENCY_FACTORS: dict[str, float] = {
    # powertrain efficiency, -15% (Dahham et al.)
    "ICE_petrol": 0.85,
    "ICE_diesel": 0.85,
    # lower inverter, motor and thermal losses, -15% (Singer et al. )
    "BEV": 0.85,
    # engine efficiency, -20% (U.S. DOE )
    "bus_ICE_diesel": 0.80,
    # drivetrain efficiency, -12.5% (ICCT )
    "bus_BEV": 0.875,
    # traction efficiency, -12.5% (IEA ETP 2023, UIC )
    "tram_metro": 0.875,
    # traction efficiency, -15%
    "train": 0.85,
# demandreductioncircularity: heavy-duty trucks
    # engine efficiency, -20%
    "HDT_diesel": 0.80,
    # drivetrain efficiency, -12.5%
    "HDT_BET": 0.875,
    # system efficiency, -20%
    "HDT_FCEV": 0.80,
    # demandreductioncircularity: ships
    # propulsion efficiency, -20%
    "diesel_ICE_ship": 0.80,
    # propulsion efficiency, -15%
    "methanol_ICE_ship": 0.85,
    # propulsion efficiency, -15%
    "ammonia_ICE_ship": 0.85,
    # stack and balance-of-plant efficiency, -15% ; applied to the
    # hydrogen and to the electricity for its liquefaction
    "hydrogen_FC_ship": 0.85,
}
def demand_reduction_scenarios(carrier_name: str) -> list[Scenario]:
    """Return the demand scenarios of a carrier, applied as a factor on the demand.

    Args:
        carrier_name: Name of the carrier, e.g. 'steel'.

    Returns:
        list[Scenario]: One scenario per entry in DEMAND_FACTORS, empty if the
            carrier has no demand scenarios.
    """
    return [
        Scenario(name, file_op=factor)
        for name, factor in DEMAND_FACTORS.get(carrier_name, {}).items()
    ]
# demandreductioncircularity: helper for the efficiency scenarios
def scale_conversion_factor(
    conversion_factor: list[dict], factors: dict[str, float]
) -> list[dict]:
    """Return a copy of a conversion factor with some carriers scaled.

    Args:
        conversion_factor: The default value of a conversion factor, a list of
            {carrier: {"default_value": ..., "unit": ...}}.
        factors: The factor per carrier, e.g. {"electricity": 0.9}. Carriers
            that are not listed keep their value.

    Returns:
        list[dict]: The scaled conversion factor.
    """
    return [
        {
            carrier: (
                {**value, "default_value": value["default_value"] * factors[carrier]}
                if carrier in factors
                else value
            )
            for carrier, value in entry.items()
        }
        for entry in conversion_factor
    ]
# demandreductioncircularity: helper for the efficiency scenarios of vehicles
def efficiency_scenario(conversion_factor: list[dict], technology: str) -> Scenario:
    """Return the efficiency improvements scenario of a vehicle or ship.

    All input carriers of the conversion factor are scaled with the factor of
    the technology in TRANSPORT_EFFICIENCY_FACTORS.

    Args:
        conversion_factor: The default value of the conversion factor.
        technology: Name of the technology, e.g. 'HDT_diesel'.

    Returns:
        Scenario: The efficiency improvements scenario.
    """
    factor = TRANSPORT_EFFICIENCY_FACTORS[technology]
    carriers = {carrier: factor for entry in conversion_factor for carrier in entry}
    return Scenario(
        EFFICIENCY_IMPROVEMENTS,
        default_value=scale_conversion_factor(conversion_factor, carriers),
    )

# demandreductioncircularity: helper for the input share constraints
def input_share_series(element, carrier: str, value: float, name: str):
    """Return an input share as a Series over carrier, node and year.

       The tech_share_limits plugin reads input_share_min/max per input carrier,
       so the share only applies to the named carrier (not to e.g. electricity).

       Args:
           element: The conversion technology.
           carrier: The input carrier the share applies to, e.g. 'plastic_waste'.
           value: The share (0-1).
           name: The attribute name, used as the value column of the csv
               (e.g. 'input_share_min').

       Returns:
           pd.Series: The share, indexed by carrier, node and year.
       """
    import pandas as pd

    index = pd.MultiIndex.from_product(
        [
            [carrier],
            list(element.model.config.system.set_nodes),
            list(element.settings.time.years),
        ],
        names=["carrier", "node", "year"],
    )
    return pd.Series(value, index=index, name=name)