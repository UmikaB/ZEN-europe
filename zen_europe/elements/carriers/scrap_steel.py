# demandreductioncircularity: new carrier scrap_steel (EAF input)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import Scenario
from zen_creator.elements import Carrier
from zen_creator.utils.attribute import Attribute

from zen_europe.datasets.dataset_collections.steel_demand import SteelDemand
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    INDUSTRIAL_CIRCULAR_PUSH,  # demandreductioncircularity
    SCRAP_STEEL_AVAILABILITY_FACTOR,  # demandreductioncircularity
)


class ScrapSteel(Carrier):
    """Scrap steel carrier class.

    Scrap steel is an input of the EAF. Its availability is limited to a share
    of the steel demand that grows over time.
    """

    name: str = "scrap_steel"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_availability_import(self) -> Attribute:
        """
        Return the import availability of scrap steel.

        """
        steel_demand = SteelDemand(source_path=self.model.source_path)
        attr = steel_demand.get_scrap_steel_availability(element=self)
        # demandreductioncircularity: industrial circular push, upper-bound JRC scrap
        attr.add_scenarios(
            Scenario(INDUSTRIAL_CIRCULAR_PUSH, file_op=SCRAP_STEEL_AVAILABILITY_FACTOR)
        )
        return attr

    def _set_availability_export(self) -> Attribute:
        """
        Return the export availability of scrap steel (unlimited).

        """
        return Attribute(
            "availability_export",
            default_value=float("inf"),
            element=self,
            unit=self.power_unit,
        )

    # price_import and price_export keep the zen-creator default of 0 (free scrap).

