# demandreductioncircularity: new technology train (regional electric trains)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import (
    Attribute,
    ConversionTechnology,
    Scenario,
)

from zen_europe.datasets.dataset_collections.circularity_demand_reduction_public_transport import (
    CircularityDemandReductionPublicTransport,
)
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    EFFICIENCY_IMPROVEMENTS,
    TRANSPORT_EFFICIENCY_FACTORS,
    scale_conversion_factor,
)


class Train(ConversionTechnology):
    """Class containing all data and assumptions for regional electric trains"""

    name: str = "train"

    def __init__(self, model: Model, power_unit: str = "megapkm/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier of train to train_mileage.
        """
        return Attribute(
            name="reference_carrier", default_value=["train_mileage"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carrier of train to electricity.
        """
        return Attribute(
            name="input_carrier", default_value=["electricity"], element=self
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Set the output carrier of train to train_mileage.
        """
        return Attribute(
            name="output_carrier", default_value=["train_mileage"], element=self
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of train.

        """
        public_transport = CircularityDemandReductionPublicTransport(self.source_path)
        return public_transport.get_lifetime(element=self)

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of train, with the efficiency improvements
        scenario

        """
        public_transport = CircularityDemandReductionPublicTransport(self.source_path)
        attr = public_transport.get_conversion_factor(element=self)
        attr.add_scenarios(
            Scenario(
                EFFICIENCY_IMPROVEMENTS,
                default_value=scale_conversion_factor(
                    attr.default_value,
                    {"electricity": TRANSPORT_EFFICIENCY_FACTORS[self.name]},
                ),
            )
        )
        return attr

    def _set_capex_specific_conversion(self) -> Attribute:
        """
        Sets the specific conversion CAPEX of train.

        """
        public_transport = CircularityDemandReductionPublicTransport(self.source_path)
        return public_transport.get_capex_specific_conversion(element=self)

    def _set_opex_specific_variable(self) -> Attribute:
        """
        Sets the specific variable OPEX of train.

        """
        public_transport = CircularityDemandReductionPublicTransport(self.source_path)
        return public_transport.get_opex_specific_variable(element=self)

    def _set_opex_specific_fixed(self) -> Attribute:
        """
        Sets the specific fixed OPEX of train.

        """
        public_transport = CircularityDemandReductionPublicTransport(self.source_path)
        return public_transport.get_opex_specific_fixed(element=self)
