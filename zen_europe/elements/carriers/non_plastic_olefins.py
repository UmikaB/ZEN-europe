# demandreductioncircularity: new carrier non_plastic_olefins (final demand)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier
from zen_creator.utils.attribute import Attribute

from zen_europe.datasets.dataset_collections.olefin_demand import OlefinDemand
from zen_europe.utils.demand_sensitivity import demand_sensitivity_scenarios


class NonPlasticOlefins(Carrier):
    """Non-plastic olefins carrier class.

    Final demand for olefins not used for plastics, met by
    olefins_to_nonplastics.
    """

    name: str = "non_plastic_olefins"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_demand(self) -> Attribute:
        """
        Return the demand of non-plastic olefins.

        """
        olefin_demand = OlefinDemand(
            source_path=self.model.source_path, settings=self.settings
        )
        attr = olefin_demand.get_non_plastic_olefin_demand(element=self)
        if self.settings.scenario.sensitivity_demand:
            attr.add_scenarios(demand_sensitivity_scenarios(self.name))
        return attr
