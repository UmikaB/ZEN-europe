# demandreductioncircularity: new dummy technology raw material -> clinker input
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology, Scenario

from zen_europe.datasets.datasets.technology.ecra_technology_papers import (
    ECRATechnologyPapers,
)
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    EFFICIENCY_IMPROVEMENTS,
    RAW_MATERIAL_FOR_CLINKER_FACTOR,
    scale_conversion_factor,
)


class RawMaterialForClinker(ConversionTechnology):
    """Dummy technology that turns virgin raw material (limestone, clay, shale)
    into clinker input material."""

    name: str = "raw_material_for_clinker"

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
        Sets the input carrier to raw material for clinker.
        """
        return Attribute(
            name="input_carrier", default_value=["raw_material_clinker"], element=self
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
        Sets the lifetime of raw material for clinker.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=100,
            source=AssumptionInformation(
                description=(
                    "Dummy technology without costs; lifetime of 100 years, "
                    "assumption"
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of raw material for clinker.

        Efficiency improvements: raw meal preparation -15%.
        """
        ecra_dataset = ECRATechnologyPapers(source_path=self.source_path)
        attr = ecra_dataset.get_conversion_factor_raw_material_for_clinker(self)
        attr.add_scenarios(
            Scenario(
                EFFICIENCY_IMPROVEMENTS,
                default_value=scale_conversion_factor(
                    attr.default_value,
                    {"raw_material_clinker": RAW_MATERIAL_FOR_CLINKER_FACTOR},
                ),
            )
        )
        return attr
