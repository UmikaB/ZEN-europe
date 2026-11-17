from __future__ import annotations

from typing import TYPE_CHECKING

#from zen_europe.datasets.dataset_collections.olefin_demand import OlefinDemand
#from zen_europe.utils.demand_sensitivity import demand_sensitivity_scenarios
from zen_creator import AssumptionInformation  # demandreductioncircularity

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier
from zen_creator.utils.attribute import Attribute


class Olefin(Carrier):
    """Olefin carrier class.

    This class implements the specific behavior for the olefin carrier.
    """

    name: str = "olefin"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ----Example of optional methods for overriding default attributes ------

    def _set_availability_import(self) -> Attribute:
        """
        Return the import availability of olefin.

        """
        return Attribute(
            "availability_import",
            default_value=0,
            element=self,
            unit=self.power_unit,
        )

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

    # demandreductioncircularity: demand moved to plastic_use and non_plastic_olefin
    def _set_demand(self) -> Attribute:
        """
        Return the demand of olefin.

        The final demand is placed on the plastic_use and non_plastic_olefins
         carriers, so the olefin demand is 0.
     """
        attr = self.demand
        attr.set_data(
            default_value=0,
            source=AssumptionInformation(
                description=(
                    "The final olefin demand is split into plastic use and "
                    "non-plastic olefins, so olefin has no demand of its own  "
                ),
            ),
        )
        return attr

