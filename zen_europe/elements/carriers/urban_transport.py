# demandreductioncircularity: new carrier urban_transport (final demand)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier
from zen_creator.utils.attribute import Attribute

from zen_europe.datasets.dataset_collections.circularity_demand_reduction_passenger_transport import (  # noqa: E501
    CircularityDemandReductionPassengerTransport,
)
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    demand_reduction_scenarios,
)
from zen_europe.utils.demand_sensitivity import demand_sensitivity_scenarios


class UrbanTransport(Carrier):
    """UrbanTransport carrier class.

    Final demand for urban passenger transport (trips below 100 km)
    in passenger-km: buses, trams/metros and 50% of the car passenger-km.
    """

    name: str = "urban_transport"

    def __init__(self, model: Model, power_unit: str = "pkm/h"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_demand(self) -> Attribute:
        """
        Return the hourly demand of urban_transport.

        """
        passenger_transport = CircularityDemandReductionPassengerTransport(
            self.settings, self.source_path
        )
        attr = passenger_transport.get_demand(self)
        # scenarios 1, 4 and 5 (thesis Tables 3.5, 3.8 and 3.9)
        attr.add_scenarios(demand_reduction_scenarios(self.name))
        if self.settings.scenario.sensitivity_demand:
            attr.add_scenarios(demand_sensitivity_scenarios(self.name))
        return attr

    def _set_price_shed_demand(self) -> Attribute:
        """
        Return the price of shed demand of the carrier.

        """
        if self.settings.availability.allow_all_demand_shedding:
            return Attribute(
                "price_shed_demand",
                default_value=1e4,
                element=self,
                unit="Euro/pkm",
            )
        else:
            return self.price_shed_demand

    def _set_availability_import(self) -> Attribute:
        """
        Return the availability of import of the carrier (none).

        """
        return Attribute(
            "availability_import",
            default_value=0,
            element=self,
            unit="pkm/h",
        )
