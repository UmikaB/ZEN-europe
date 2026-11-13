# demandreductioncircularity: new dummy technology secondary_steel -> steel
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

import pandas as pd
from zen_creator import AssumptionInformation, Attribute, ConversionTechnology, Scenario

from zen_europe.datasets.datasets.carrier.circularity_demand_reduction_scrap_steel_jrc import (  # noqa: E501
    CircularityDemandReductionScrapSteelJRC,  # demandreductioncircularity
)
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    INDUSTRIAL_CIRCULAR_PUSH,  # demandreductioncircularity
)

class SecondarySteelToSteel(ConversionTechnology):
    """Dummy technology that turns secondary steel into the final steel
    product, so that primary and secondary steel together meet one steel
    demand."""

    name: str = "secondary_steel_to_steel"

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
        Sets the input carrier to secondary steel.
        """
        return Attribute(
            name="input_carrier", default_value=["secondary_steel"], element=self
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carrier to steel.
        """
        return Attribute(name="output_carrier", default_value=["steel"], element=self)

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of secondary steel to steel.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=20,
            source=AssumptionInformation(
                description=(
                    "Dummy technology without costs; the lifetime of 20 years is an assumption and irrelevant as this is a dummy technology."
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of secondary steel to steel.

        One ton of secondary steel gives one ton of steel.
        """
        attr = self.conversion_factor
        attr.set_data(
            default_value=[
                {"secondary_steel": {"default_value": 1.0, "unit": "tproduct/tproduct"}}
            ],
            source=AssumptionInformation(
                description=(
                    "Dummy technology: one ton of secondary steel gives one ton of "
                    "steel."
                ),
            ),
        )
        return attr
   # demandreductioncircularity: secondary steel share (JRC), min = max
    def _set_demand_share_min(self) -> Attribute:
        """
        Return the minimum share of the steel demand met by secondary steel.

        Industrial circular push: no minimum share (thesis Table 3.6).
        """
        jrc_dataset = CircularityDemandReductionScrapSteelJRC(
            source_path=self.model.source_path
        )
        attr = jrc_dataset.get_demand_share(self, self.demand_share_min)
        attr.add_scenarios(
            Scenario(
                INDUSTRIAL_CIRCULAR_PUSH,
                df=pd.Series(0.0, index=attr.df.index, name=attr.name),
            )
        )
        return attr

    # demandreductioncircularity: secondary steel share (JRC), min = max
    def _set_demand_share_max(self) -> Attribute:
        """
        Return the maximum share of the steel demand met by secondary steel.

        Industrial circular push: no maximum share (thesis Table 3.6); the split
        is then limited by the scrap availability only.
        """
        jrc_dataset = CircularityDemandReductionScrapSteelJRC(
            source_path=self.model.source_path
        )
        attr = jrc_dataset.get_demand_share(self, self.demand_share_max)
        attr.add_scenarios(
            Scenario(
                INDUSTRIAL_CIRCULAR_PUSH,
                df=pd.Series(float("inf"), index=attr.df.index, name=attr.name),
            )
        )
        return attr