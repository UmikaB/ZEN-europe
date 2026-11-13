# demandreductioncircularity: new dummy technology concrete fines -> clinker input
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology

from zen_europe.datasets.datasets.technology.circularity_demand_reduction_cement_fines_cembureau import (  # noqa: E501
    CircularityDemandReductionCementFinesCembureau,
)


class CementFinesForClinker(ConversionTechnology):
    """Dummy technology that turns recycled concrete fines into clinker input
    material."""

    name: str = "cement_fines_for_clinker"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to clinker input material.
        """
        return Attribute(
            name="reference_carrier",
            default_value=["clinker_input_material"],
            element=self,
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carrier to concrete fines.
        """
        return Attribute(
            name="input_carrier", default_value=["concrete_fine"], element=self
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carrier to clinker input material.
        """
        return Attribute(
            name="output_carrier",
            default_value=["clinker_input_material"],
            element=self,
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of cement fines for clinker.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=100,
            source=AssumptionInformation(
                description=(
                    "Dummy technology without costs; lifetime of 100 years, "
                    "assumption."
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of cement fines for clinker.

        """
        cembureau_dataset = CircularityDemandReductionCementFinesCembureau(
            source_path=self.source_path
        )
        return cembureau_dataset.get_conversion_factor_cement_fines_for_clinker(self)
