# demandreductioncircularity: new technology plastic waste -> electricity
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology

from zen_europe.datasets.datasets.technology.circularity_demand_reduction_incineration_plastic_eunomia import (  # noqa: E501
    CircularityDemandReductionIncinerationPlasticEunomia,
)


class IncinerationPlastic(ConversionTechnology):
    """Incineration of plastic waste with electricity recovery."""

    name: str = "incineration_plastic"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to electricity.
        """
        return Attribute(
            name="reference_carrier", default_value=["electricity"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carrier to plastic waste.
        """
        return Attribute(
            name="input_carrier", default_value=["plastic_waste"], element=self
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carrier to electricity (no heat, as for waste_plant).
        """
        return Attribute(
            name="output_carrier", default_value=["electricity"], element=self
        )

    # ---------- Required methods that are called during object build ----------

    def _eunomia(self) -> CircularityDemandReductionIncinerationPlasticEunomia:
        return CircularityDemandReductionIncinerationPlasticEunomia(
            source_path=self.source_path
        )

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of plastic incineration.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=35,
            source=AssumptionInformation(
                description=(
                    "Lifetime of 35 years, assumption "
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of plastic incineration.

        """
        return self._eunomia().get_conversion_factor(self)

    def _set_capex_specific_conversion(self) -> Attribute:
        """
        Sets the specific capex of plastic incineration.

        """
        return self._eunomia().get_capex_specific_conversion(self)

    def _set_opex_specific_fixed(self) -> Attribute:
        """
        Sets the specific fixed opex of plastic incineration.

        """
        return self._eunomia().get_opex_specific_fixed(self)

    def _set_opex_specific_variable(self) -> Attribute:
        """
        Sets the specific variable opex of plastic incineration, the same as
        the waste plant.

        """
        waste_plant = self.model.conversion_technologies["waste_plant"]
        reference = waste_plant.opex_specific_variable
        attr = self.opex_specific_variable
        attr.set_data(
            default_value=reference.default_value,
            unit=reference.unit,
            source=AssumptionInformation(
                description=(
                    "Variable opex assumed the same as for the waste plant"
                ),
            ),
        )
        return attr

    # carbon_intensity_technology keeps the default of 0, as in the thesis (see
    # the Excel overview: plastic incineration emits fossil CO2 in reality).
