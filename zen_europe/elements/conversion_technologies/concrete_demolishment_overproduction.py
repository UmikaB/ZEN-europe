# demandreductioncircularity: new dummy technology concrete -> use + waste
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology

from zen_europe.datasets.datasets.carrier.circularity_demand_reduction_concrete_waste_eea import (
    CircularityDemandReductionConcreteWasteEEA,
)


class ConcreteDemolishmentOverproduction(ConversionTechnology):
    """Dummy technology that splits concrete into concrete use (final demand)
    and concrete waste (demolition and overproduction)."""

    name: str = "concrete_demolishment_overproduction"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to concrete use.
        """
        return Attribute(
            name="reference_carrier", default_value=["concrete_use"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carrier to concrete.
        """
        return Attribute(name="input_carrier", default_value=["concrete"], element=self)

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carriers to concrete use and concrete waste.
        """
        return Attribute(
            name="output_carrier",
            default_value=["concrete_use", "concrete_waste"],
            element=self,
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of concrete demolishment.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=20,
            source=AssumptionInformation(
                description=(
                    "Dummy technology without costs; lifetime of 20 years, "
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of concrete demolishment.

        """
        eea_dataset = CircularityDemandReductionConcreteWasteEEA(
            source_path=self.source_path
        )
        return eea_dataset.get_conversion_factor_concrete_demolishment(self)
