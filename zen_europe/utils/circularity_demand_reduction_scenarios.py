# demandreductioncircularity: new file, scenarios of the MSc thesis of U. Bhagole
"""Scenarios for demand reduction and circularity strategies.

The five scenarios of the MSc thesis of U. Bhagole (Section 3.3, Table 3.6).
Each scenario is applied on top of the reference by changing a few
attributes. All variations of one scenario share the same name, so ZEN-garden
runs them together as one scenario.

The factors are listed per carrier or technology below and are used by the
elements, see e.g. ``elements/carriers/steel.py``.
"""

from zen_creator import Scenario

# scenario names (thesis Section 3.3)
COMPACT_CITIES = "compact_cities"  # 3.3.2
INDUSTRIAL_CIRCULAR_PUSH = "industrial_circular_push"  # 3.3.3
EFFICIENCY_IMPROVEMENTS = "efficiency_improvements"  # 3.3.4
CONSUMER_DEMAND_REDUCTION = "consumer_demand_reduction"  # 3.3.5
CRISIS = "crisis"  # 3.3.6

# factors on the final demand of a carrier, per scenario
DEMAND_FACTORS: dict[str, dict[str, float]] = {
    "steel": {
        # material efficiency: -10% (Material Economics 2019 [110])
        INDUSTRIAL_CIRCULAR_PUSH: 0.90,
        # longer lifetimes, repair and reuse: -5% ([110], worldsteel 2023 [140])
        CONSUMER_DEMAND_REDUCTION: 0.95,
        # reduced steel output: -25% ([145])
        CRISIS: 0.75,
    },
}

# industrial circular push: scrap steel availability from the upper-bound JRC
# projection (secondary steel ~70% above 2018, ~77% share in 2050) instead of
# the lower bound (JRC 2021 [77])
SCRAP_STEEL_AVAILABILITY_FACTOR = 1.29

# efficiency improvements: EAF process efficiency, -15% electricity per tonne
# of crude steel (Material Economics 2019 [110])
EAF_ELECTRICITY_FACTOR = 0.85


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
