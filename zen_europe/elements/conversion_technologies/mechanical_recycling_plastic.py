# demandreductioncircularity: new technology plastic waste -> plastic (mechanical)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import (
    AssumptionInformation,
    Attribute,
    ConversionTechnology,
    Scenario,
    SourceInformation,
)

from zen_europe.datasets.datasets.carrier.circularity_demand_reduction_plastic_waste_plastics_europe import (  # noqa: E501
    CircularityDemandReductionPlasticWastePlasticsEurope,
)
from zen_europe.datasets.datasets.carrier.circularity_demand_reduction_plastic_waste_saputra_lase import (  # noqa: E501
    CircularityDemandReductionPlasticWasteSaputraLase,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_mechanical_recycling_plastic_larrain import (  # noqa: E501
    CircularityDemandReductionMechanicalRecyclingPlasticLarrain,
)
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    INDUSTRIAL_CIRCULAR_PUSH,
    input_share_series,
)


class MechanicalRecyclingPlastic(ConversionTechnology):
    """Mechanical recycling of plastic waste into new plastic."""

    name: str = "mechanical_recycling_plastic"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to plastic.
        """
        return Attribute(
            name="reference_carrier", default_value=["plastic"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carriers to plastic waste and electricity.
        """
        return Attribute(
            name="input_carrier",
            default_value=["plastic_waste", "electricity"],
            element=self,
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carrier to plastic.
        """
        return Attribute(name="output_carrier", default_value=["plastic"], element=self)

    # ---------- Required methods that are called during object build ----------

    def _larrain(self) -> CircularityDemandReductionMechanicalRecyclingPlasticLarrain:
        return CircularityDemandReductionMechanicalRecyclingPlasticLarrain(
            source_path=self.source_path
        )

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of mechanical recycling.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=35,
            source=AssumptionInformation(
                description=(
                    "Lifetime of 35 years (assumption) "
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of mechanical recycling.

        """
        return self._larrain().get_conversion_factor(self)

    def _set_capex_specific_conversion(self) -> Attribute:
        """
        Sets the specific capex of mechanical recycling.

        """
        return self._larrain().get_capex_specific_conversion(self)

    def _set_opex_specific_fixed(self) -> Attribute:
        """
        Sets the specific fixed opex of mechanical recycling.

        """
        return self._larrain().get_opex_specific_fixed(self)

    def _set_opex_specific_variable(self) -> Attribute:
        """
        Sets the specific variable opex of mechanical recycling.

        """
        return self._larrain().get_opex_specific_variable(self)

    def _set_input_share_min(self) -> Attribute:
        """
        Return the minimum share of the plastic waste used by mechanical
        recycling.

        Reference: 26.8% (min = max, today's share kept constant). Industrial
        circular push: at least 46%.
        """
        today = CircularityDemandReductionPlasticWastePlasticsEurope(
            source_path=self.source_path
        )
        improved = CircularityDemandReductionPlasticWasteSaputraLase(
            source_path=self.source_path
        )
        share = today.get_recycling_share(self.name)
        share_s2 = improved.get_recycling_share(self.name)
        attr = self.input_share_min
        attr.set_data(
            df=input_share_series(self, "plastic_waste", share, "input_share_min"),
            unit="1",
            source=SourceInformation(
                description=(
                    f"Reference: mechanical recycling treats exactly {share:.1%} of "
                    "the plastic waste (EU27+3 in 2022), kept constant over time."
                ),
                metadata=today.metadata,
            ),
        )
        attr.add_scenarios(
            Scenario(
                INDUSTRIAL_CIRCULAR_PUSH,
                df=input_share_series(
                    self, "plastic_waste", share_s2, "input_share_min"
                ),
            )
        )
        attr.add_source(
            SourceInformation(
                description=(
                    f"Industrial circular push: mechanical recycling treats at least "
                    f"{share_s2:.0%} of the plastic waste (JRC improved scenario)."
                ),
                metadata=improved.metadata,
            )
        )
        return attr

    def _set_input_share_max(self) -> Attribute:
        """
        Return the maximum share of the plastic waste used by mechanical
        recycling.

        Reference: 26.8% (min = max). Industrial circular push: no upper limit
        (share 1), as in the model input of the thesis.
        """
        today = CircularityDemandReductionPlasticWastePlasticsEurope(
            source_path=self.source_path
        )
        share = today.get_recycling_share(self.name)
        attr = self.input_share_max
        attr.set_data(
            df=input_share_series(self, "plastic_waste", share, "input_share_max"),
            unit="1",
            source=SourceInformation(
                description=(
                    f"Reference: mechanical recycling treats at most {share:.1%} of "
                    "the plastic waste (EU27+3 in 2022), kept constant over time."
                ),
                metadata=today.metadata,
            ),
        )
        attr.add_scenarios(
            Scenario(
                INDUSTRIAL_CIRCULAR_PUSH,
                df=input_share_series(self, "plastic_waste", 1.0, "input_share_max"),
            )
        )
        attr.add_source(
            AssumptionInformation(
                description=(
                    "Industrial circular push: no upper limit on mechanical recycling"
                ),
            )
        )
        return attr

