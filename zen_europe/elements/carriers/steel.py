# demandreductioncircularity: new carrier steel (total steel demand)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier
from zen_creator.utils.attribute import Attribute

from zen_europe.datasets.dataset_collections.steel_demand import SteelDemand
from zen_europe.utils.demand_sensitivity import demand_sensitivity_scenarios


class Steel(Carrier):
    """Steel carrier class.

    Final steel product. The total steel demand is placed on this carrier and
    can be met by primary steel (primary_steel_to_steel) or secondary steel
    (secondary_steel_to_steel).
    """

    name: str = "steel"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_availability_import(self) -> Attribute:
        """
        Return the import availability of steel.

        """
        return Attribute(
            "availability_import",
            default_value=0,
            element=self,
            unit=self.power_unit,
        )

    # availability_export keeps the zen-creator default of 0.

    def _set_price_shed_demand(self) -> Attribute:
        """
        Return the price of shed demand of the carrier.

        """
        if self.settings.availability.allow_all_demand_shedding:
            return Attribute(
                "price_shed_demand",
                default_value=1e4,
                element=self,
                unit="Euro/tproduct",
            )
        else:
            return self.price_shed_demand

    def _set_demand(self) -> Attribute:
        """
        Return the total steel demand.

        """
        steel_demand = SteelDemand(source_path=self.model.source_path)
        attr = steel_demand.get_steel_demand(element=self)
        if self.settings.scenario.sensitivity_demand:
            attr.add_scenarios(demand_sensitivity_scenarios(self.name))
        return attr
