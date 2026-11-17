# demandreductioncircularity: new dummy technology plastic -> plastic use + waste
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology

from zen_europe.datasets.datasets.carrier.circularity_demand_reduction_plastic_waste_plastics_europe import (  # noqa: E501
    CircularityDemandReductionPlasticWastePlasticsEurope,
)


class OverproductionUsePlastic(ConversionTechnology):
    """Dummy technology that splits plastic into plastic use (final demand) and
    plastic waste."""

    name: str = "overproduction_use_plastic"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to plastic use.
        """
        return Attribute(
            name="reference_carrier", default_value=["plastic_use"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carrier to plastic.
        """
        return Attribute(name="input_carrier", default_value=["plastic"], element=self)

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carriers to plastic use and plastic waste.
        """
        return Attribute(
            name="output_carrier",
            default_value=["plastic_use", "plastic_waste"],
            element=self,
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
                    "Dummy technology without costs; lifetime of 100 years "
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of overproduction and use of plastic.

        """
        plastics_europe = CircularityDemandReductionPlasticWastePlasticsEurope(
            source_path=self.source_path
        )
        return plastics_europe.get_conversion_factor_overproduction_use_plastic(self)
