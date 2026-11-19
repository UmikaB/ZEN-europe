# demandreductioncircularity: new dummy technology passenger_mileage -> urban_transport
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology, Scenario

from zen_europe.datasets.dataset_collections.circularity_demand_reduction_passenger_transport import (  # noqa: E501
    CircularityDemandReductionPassengerTransport,
)
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    COMPACT_CITIES,
    COMPACT_CITIES_CAR_SHARE_FACTOR,
)


class CarPassengerMileageToUrban(ConversionTechnology):
    """Dummy technology that converts passenger_mileage 1:1 into
    urban_transport, without cost or losses """

    name: str = "car_passenger_mileage_to_urban"

    def __init__(self, model: Model, power_unit: str = "megapkm/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to urban_transport.
        """
        return Attribute(
            name="reference_carrier", default_value=["urban_transport"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carrier to passenger_mileage.
        """
        return Attribute(
            name="input_carrier", default_value=["passenger_mileage"], element=self
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carrier to urban_transport.
        """
        return Attribute(
            name="output_carrier", default_value=["urban_transport"], element=self
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of the dummy technology.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=100,
            source=AssumptionInformation(
                description=(
                    "Dummy technology, lifetime of 100 years "
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor: 1 pkm of passenger_mileage per pkm of
        urban_transport.

        """
        attr = self.conversion_factor
        attr.set_data(
            default_value=[
                {"passenger_mileage": {"default_value": 1.0, "unit": "pkm/pkm"}}
            ],
            source=AssumptionInformation(
                description=(
                    "Dummy technology without losses "
                ),
            ),
        )
        return attr

    def _set_capex_specific_conversion(self) -> Attribute:
        """
        Sets the specific capex of the dummy technology to 0.

        """
        attr = self.capex_specific_conversion
        attr.set_data(
            default_value=0,
            unit="Euro/(pkm/h)",
            source=AssumptionInformation(
                description=(
                    "Dummy technology without cost ."
                ),
            ),
        )
        return attr

    def _set_demand_share_min(self) -> Attribute:
        """
        Return the minimum share of urban transport by car.

        No limit in the reference. Compact cities: 50% of the 2019 urban car
        share of each country, as minimum and maximum
        """
        return self._compact_cities_share(self.demand_share_min)

    def _set_demand_share_max(self) -> Attribute:
        """
        Return the maximum share of urban transport by car.

        No limit in the reference. Compact cities: 50% of the 2019 urban car
        share of each country, as minimum and maximum.
        """
        return self._compact_cities_share(self.demand_share_max)

    def _compact_cities_share(self, attr: Attribute) -> Attribute:
        """Add the compact cities scenario to a demand share attribute."""
        passenger_transport = CircularityDemandReductionPassengerTransport(
            self.settings, self.source_path
        )
        attr.add_scenarios(
            Scenario(
                COMPACT_CITIES,
                df=passenger_transport.get_modal_share_df(
                    self, COMPACT_CITIES_CAR_SHARE_FACTOR, attr.name
                ),
            )
        )
        attr.add_source(
            AssumptionInformation(
                description=(
                    "Compact cities: the urban car share is fixed at "
                    f"{COMPACT_CITIES_CAR_SHARE_FACTOR:.0%} of each country's 2019 "
                    "share (EU Statistical Pocketbook 2022) in all years "
                ),
            )
        )
        return attr
