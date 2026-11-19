from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import AssumptionInformation
from zen_creator.elements import Carrier
from zen_creator.utils.attribute import Attribute

#from zen_europe.datasets.dataset_collections.passenger_mileage_demand import (
#)
#from zen_europe.utils.demand_sensitivity import demand_sensitivity_scenarios


class PassengerMileage(Carrier):
    """All data and assumption for passenger mileage carrier."""
    # demandreductioncircularity: passenger-km of private cars (BEV, ICE petrol,
    # ICE diesel), in pkm instead of vkm. It has no final demand any more: the
    # car passenger-km are converted into urban and regional passenger transport
    # by car_passenger_mileage_to_urban and car_passenger_mileage_to_regional

    name: str = "passenger_mileage"

    # demandreductioncircularity: pkm instead of vkm
    def __init__(self, model: Model, power_unit: str = "pkm/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ----Example of optional methods for overriding default attributes ------
    # demandreductioncircularity: the final demand sits on urban_transport and
    # regional_transport
    def _set_demand(self) -> Attribute:
        """
        Return the demand for passenger mileage (none).

        """
        attr = self.demand
        attr.set_data(
            default_value=0,
            df=None,
            unit="megapkm/hour",
            source=AssumptionInformation(
                description=(
                    "No final demand: the car passenger-km meet the demand of "
                    "urban_transport and regional_transport via "
                    "car_passenger_mileage_to_urban and "
                    "car_passenger_mileage_to_regional "
                ),
            ),
        )
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
                unit="Euro/pkm",  # demandreductioncircularity: pkm
            )
        else:
            return self.price_shed_demand

    def _set_availability_import(self) -> Attribute:
        """
        Return the availability of import of the carrier.

        """
        return Attribute(
            "availability_import",
            default_value=0,
            element=self,
            unit="pkm/h",  # demandreductioncircularity: pkm
        )
