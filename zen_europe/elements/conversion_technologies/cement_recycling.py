# demandreductioncircularity: new technology concrete waste -> cement
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

import pandas as pd
from zen_creator import (
    AssumptionInformation,
    Attribute,
    ConversionTechnology,
    Scenario,
    SourceInformation,
)

from zen_europe.datasets.dataset_collections.clinker_data import ClinkerData
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_cement_recycling_cordis import (
    CircularityDemandReductionCementRecyclingCORDIS,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_cement_recycling_kulisch import (
    CircularityDemandReductionCementRecyclingKulisch,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_cement_recycling_wits import (
    CircularityDemandReductionCementRecyclingWITS,
)
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    INDUSTRIAL_CIRCULAR_PUSH,
)


class CementRecycling(ConversionTechnology):
    """Recovery of unhydrated cement particles from concrete waste, which are
    reintroduced as cement and bypass the clinker kiln."""

    name: str = "cement_recycling"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to cement.
        """
        return Attribute(
            name="reference_carrier", default_value=["cement"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carriers to concrete waste and electricity.
        """
        return Attribute(
            name="input_carrier",
            default_value=["concrete_waste", "electricity"],
            element=self,
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carrier to cement.
        """
        return Attribute(name="output_carrier", default_value=["cement"], element=self)

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of cement recycling.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=20,
            source=AssumptionInformation(
                description=(
                    "Lifetime of 20 years, assumption."
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of cement recycling.

        """
        clinker_data = ClinkerData(source_path=self.source_path)
        return clinker_data.get_conversion_factor_cement_recycling(self)

    def _set_capex_specific_conversion(self) -> Attribute:
        """
        Sets the specific capex of cement recycling.

        """
        cordis_dataset = CircularityDemandReductionCementRecyclingCORDIS(
            source_path=self.source_path
        )
        return cordis_dataset.get_capex_specific_cement_recycling(self)

    def _set_opex_specific_variable(self) -> Attribute:
        """
        Sets the specific variable opex of cement recycling.

        """
        wits_dataset = CircularityDemandReductionCementRecyclingWITS(
            source_path=self.source_path
        )
        return wits_dataset.get_opex_specific_variable_cement_recycling(self)

    def _set_input_share_max(self) -> Attribute:
        """
        Return the maximum share of the concrete waste used by cement recycling.

        Reference: 0, since unhydrated cement recovery is not applied at scale.
        Industrial circular push: at most 21% of the concrete waste (Kulisch et
        al. 2022). The electricity input keeps the default of 1 (no limit).
        """
        years = list(self.settings.time.years)
        nodes = list(self.model.config.system.set_nodes)
        index = pd.MultiIndex.from_product(
            [["concrete_waste"], nodes, years], names=["carrier", "node", "year"]
        )
        attr = self.input_share_max
        attr.set_data(
            df=pd.Series(0.0, index=index, name=attr.name),
            unit="1",
            source=AssumptionInformation(
                description=(
                    "Unhydrated cement recovery is not yet deployed at scale, so "
                    "cement recycling may use 0% of the concrete waste in the "
                    "reference scenario"
                ),
            ),
        )
        kulisch_dataset = CircularityDemandReductionCementRecyclingKulisch(
            source_path=self.source_path
        )
        share = kulisch_dataset.get_recoverable_share()
        attr.add_scenarios(
            Scenario(
                INDUSTRIAL_CIRCULAR_PUSH,
                df=pd.Series(share, index=index, name=attr.name),
            )
        )
        attr.add_source(
            SourceInformation(
                description=(
                    f"Industrial circular push: cement recycling may use at most "
                    f"{share:.0%} of the concrete waste, the midpoint of the 6-36% "
                    "unhydrated cement in hardened concrete and paste."
                ),
                metadata=kulisch_dataset.metadata,
            )
        )
        return attr
