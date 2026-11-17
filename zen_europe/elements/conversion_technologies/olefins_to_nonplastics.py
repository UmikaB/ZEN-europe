# demandreductioncircularity: new dummy technology olefin -> non-plastic olefins
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology


class OlefinsToNonplastics(ConversionTechnology):
    """Dummy technology that allocates olefins to non-plastic uses."""

    name: str = "olefins_to_nonplastics"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to non-plastic olefins.
        """
        return Attribute(
            name="reference_carrier",
            default_value=["non_plastic_olefins"],
            element=self,
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carrier to olefin.
        """
        return Attribute(name="input_carrier", default_value=["olefin"], element=self)

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carrier to non-plastic olefins.
        """
        return Attribute(
            name="output_carrier",
            default_value=["non_plastic_olefins"],
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
                    "Dummy technology without costs; lifetime of 100 years assumption "

                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor: one ton of olefin per ton.

        """
        attr = self.conversion_factor
        attr.set_data(
            default_value=[
                {"olefin": {"default_value": 1.0, "unit": "tproduct/tproduct"}}
            ],
            source=AssumptionInformation(
                description="One ton of olefin per ton of non-plastic olefins.",
            ),
        )
        return attr
