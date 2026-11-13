from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation  # demandreductioncircularity
from zen_creator.elements import Carrier
from zen_creator.utils.attribute import Attribute

#from zen_europe.datasets.dataset_collections.clinker_data import ClinkerData
#from zen_europe.utils.demand_sensitivity import demand_sensitivity_scenarios


class Clinker(Carrier):
    """Clinker carrier class.

    This class implements the specific behavior for the clinker carrier.
    """

    name: str = "clinker"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ----Example of optional methods for overriding default attributes ------

    def _set_availability_import(self) -> Attribute:
        """
        Return the import availability of clinker.

        """
        return Attribute(
            "availability_import",
            default_value=0,
            element=self,
            unit=self.power_unit,
        )

        # demandreductioncircularity: demand moved to the concrete_use carrier

    def _set_demand(self) -> Attribute:
        """
        Return the demand of clinker.

        The final demand is placed on the concrete_use carrier, so the clinker
        demand is 0. Clinker reaches the concrete demand via clinker_to_cement,
        cement_to_concrete and concrete_demolishment_overproduction.
        """
        # demandreductioncircularity: demand is 0, see concrete_use carrier
        attr = self.demand
        attr.set_data(
            default_value=0,
            source=AssumptionInformation(
                description=(
                    "The final demand of the cement sector is placed on the "
                    "concrete_use carrier, so clinker has no demand of its own"
                ),
            ),
        )
        return attr