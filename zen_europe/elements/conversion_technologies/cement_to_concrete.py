# demandreductioncircularity: new technology cement -> concrete
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology

from zen_europe.datasets.dataset_collections.clinker_data import ClinkerData


class CementToConcrete(ConversionTechnology):
    """Production of ready-mixed concrete from cement."""

    name: str = "cement_to_concrete"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to concrete.
        """
        return Attribute(
            name="reference_carrier", default_value=["concrete"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carriers to cement and electricity.
        """
        return Attribute(
            name="input_carrier",
            default_value=["cement", "electricity"],
            element=self,
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carrier to concrete.
        """
        return Attribute(
            name="output_carrier", default_value=["concrete"], element=self
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of cement to concrete.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=20,
            source=AssumptionInformation(
                description=(
                    "Lifetime of 20 years, assumption"
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of cement to concrete.

        """
        clinker_data = ClinkerData(source_path=self.source_path)
        return clinker_data.get_conversion_factor_cement_to_concrete(self)

    def _set_capex_specific_conversion(self) -> Attribute:
        """
        Sets the specific capex of cement to concrete to 0.

        """
        attr = self.capex_specific_conversion
        attr.set_data(
            default_value=0,
            unit="Euro/(tproduct/h)",
            source=AssumptionInformation(
                description=(
                    "Concrete production is a necessary step without alternatives, "
                    "so no capex is applied."
                ),
            ),
        )
        return attr
