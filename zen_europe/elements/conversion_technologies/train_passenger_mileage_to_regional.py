# demandreductioncircularity: new dummy technology train_mileage -> regional_transport
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology

from zen_europe.datasets.dataset_collections.circularity_demand_reduction_passenger_transport import (  # noqa: E501
    CircularityDemandReductionPassengerTransport,
)


class TrainPassengerMileageToRegional(ConversionTechnology):
    """Dummy technology that converts train_mileage 1:1 into
    regional_transport, without cost or losses.
    """

    name: str = "train_passenger_mileage_to_regional"

    def __init__(self, model: Model, power_unit: str = "megapkm/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to regional_transport.
        """
        return Attribute(
            name="reference_carrier", default_value=["regional_transport"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carrier to train_mileage.
        """
        return Attribute(
            name="input_carrier", default_value=["train_mileage"], element=self
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carrier to regional_transport.
        """
        return Attribute(
            name="output_carrier", default_value=["regional_transport"], element=self
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
        Return the conversion factor: 1 pkm of train_mileage per pkm of
        regional_transport.

        """
        attr = self.conversion_factor
        attr.set_data(
            default_value=[
                {"train_mileage": {"default_value": 1.0, "unit": "pkm/pkm"}}
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
                    "Dummy technology without cost "
                ),
            ),
        )
        return attr

    def _set_demand_share_min(self) -> Attribute:
        """
        Return the minimum share of this mode in its passenger transport demand:
        its 2019 modal share - 10%.
        """
        passenger_transport = CircularityDemandReductionPassengerTransport(
            self.settings, self.source_path
        )
        return passenger_transport.get_demand_share(self, self.demand_share_min, "min")

    def _set_demand_share_max(self) -> Attribute:
        """
        Return the maximum share of this mode in its passenger transport demand:
        its 2019 modal share + 10%.
        """
        passenger_transport = CircularityDemandReductionPassengerTransport(
            self.settings, self.source_path
        )
        attr = passenger_transport.get_demand_share(self, self.demand_share_max, "max")
        return attr
