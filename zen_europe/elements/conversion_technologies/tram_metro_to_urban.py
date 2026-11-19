# demandreductioncircularity: new dummy technology tram_metro_mileage -> urban_transport
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

import pandas as pd
from zen_creator import AssumptionInformation, Attribute, ConversionTechnology, Scenario

from zen_europe.datasets.dataset_collections.circularity_demand_reduction_passenger_transport import (  # noqa: E501
    CircularityDemandReductionPassengerTransport,
)
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    COMPACT_CITIES,
)


class TramMetroToUrban(ConversionTechnology):
    """Dummy technology that converts tram_metro_mileage 1:1 into
    urban_transport, without cost or losses """

    name: str = "tram_metro_to_urban"

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
        Sets the input carrier to tram_metro_mileage.
        """
        return Attribute(
            name="input_carrier", default_value=["tram_metro_mileage"], element=self
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
        Return the conversion factor: 1 pkm of tram_metro_mileage per pkm of
        urban_transport.

        """
        attr = self.conversion_factor
        attr.set_data(
            default_value=[
                {"tram_metro_mileage": {"default_value": 1.0, "unit": "pkm/pkm"}}
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

    def _set_opex_specific_fixed(self) -> Attribute:
        """
        Sets the specific fixed opex of the dummy technology to 0.

        """
        attr = self.opex_specific_fixed
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

        Compact cities: no maximum, to allow a shift to public transport.
        """
        passenger_transport = CircularityDemandReductionPassengerTransport(
            self.settings, self.source_path
        )
        attr = passenger_transport.get_demand_share(self, self.demand_share_max, "max")
        attr.add_scenarios(
            Scenario(
                COMPACT_CITIES,
                df=pd.Series(float("inf"), index=attr.df.index, name=attr.name),
            )
        )
        return attr
