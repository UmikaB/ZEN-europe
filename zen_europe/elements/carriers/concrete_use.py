# demandreductioncircularity: new carrier concrete_use (final concrete demand)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier
from zen_creator.utils.attribute import Attribute

from zen_europe.datasets.dataset_collections.clinker_data import ClinkerData
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    demand_reduction_scenarios,
)
from zen_europe.utils.demand_sensitivity import demand_sensitivity_scenarios


class ConcreteUse(Carrier):
    """Concrete use carrier class.

    Final concrete demand of each country, met by
    concrete_demolishment_overproduction. Replaces the clinker demand.
    """

    name: str = "concrete_use"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_demand(self) -> Attribute:
        """
        Return the demand of concrete use.

        """
        clinker_data = ClinkerData(source_path=self.source_path)
        attr = clinker_data.get_concrete_demand(element=self)
        # scenarios 2 and 5 (thesis Tables 3.6 and 3.9)
        attr.add_scenarios(demand_reduction_scenarios(self.name))
        if self.settings.scenario.sensitivity_demand:
            attr.add_scenarios(demand_sensitivity_scenarios(self.name))
        return attr
