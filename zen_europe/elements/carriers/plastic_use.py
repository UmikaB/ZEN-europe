# demandreductioncircularity: new carrier plastic_use (final plastic demand)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier
from zen_creator.utils.attribute import Attribute

from zen_europe.datasets.dataset_collections.olefin_demand import OlefinDemand
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    demand_reduction_scenarios,
)
from zen_europe.utils.demand_sensitivity import demand_sensitivity_scenarios


class PlasticUse(Carrier):
    """Plastic use carrier class.

    Final plastic demand of each country, met by overproduction_use_plastic.
    """

    name: str = "plastic_use"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_demand(self) -> Attribute:
        """
        Return the demand of plastic use.

        """
        olefin_demand = OlefinDemand(
            source_path=self.model.source_path, settings=self.settings
        )
        attr = olefin_demand.get_plastic_use_demand(element=self)
        # scenarios ndustrial circular push, consumer demand reduction and crisis msc thesis U.Bhagole
        attr.add_scenarios(demand_reduction_scenarios(self.name))
        if self.settings.scenario.sensitivity_demand:
            attr.add_scenarios(demand_sensitivity_scenarios(self.name))
        return attr
