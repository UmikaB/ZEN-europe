# demandreductioncircularity: new dummy technology primary_steel -> steel
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology


class PrimarySteelToSteel(ConversionTechnology):
    """Dummy technology that turns primary steel into the final steel
    product, so that primary and secondary steel together meet one steel
    demand."""

    name: str = "primary_steel_to_steel"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to steel.
        """
        return Attribute(
            name="reference_carrier", default_value=["steel"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carrier to primary steel.
        """
        return Attribute(
            name="input_carrier", default_value=["primary_steel"], element=self
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carrier to steel.
        """
        return Attribute(name="output_carrier", default_value=["steel"], element=self)

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of primary steel to steel.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=20,
            source=AssumptionInformation(
                description=(
                    "Dummy technology without costs; the lifetime of 20 years is an assumption and irrelevant due as this is a dummy technology."
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of primary steel to steel.

        One ton of primary steel gives one ton of steel.
        """
        attr = self.conversion_factor
        attr.set_data(
            default_value=[
                {"primary_steel": {"default_value": 1.0, "unit": "tproduct/tproduct"}}
            ],
            source=AssumptionInformation(
                description=(
                    "Dummy technology: one ton of primary steel gives one ton of "
                    "steel."
                ),
            ),
        )
        return attr
