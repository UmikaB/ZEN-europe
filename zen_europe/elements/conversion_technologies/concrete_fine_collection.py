# demandreductioncircularity: new technology concrete waste -> concrete fines
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology

from zen_europe.datasets.datasets.carrier.circularity_demand_reduction_concrete_li import (
    CircularityDemandReductionConcreteLi,
)


class ConcreteFineCollection(ConversionTechnology):
    """Processing of concrete waste into concrete fines, which can replace raw
    material for clinker."""

    name: str = "concrete_fine_collection"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to concrete fines.
        """
        return Attribute(
            name="reference_carrier", default_value=["concrete_fine"], element=self
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
        Sets the output carrier to concrete fines.
        """
        return Attribute(
            name="output_carrier", default_value=["concrete_fine"], element=self
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of concrete fine collection.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=20,
            source=AssumptionInformation(
                description=(
                    "Lifetime of 20 years, assumption (model input of the MSc "
                    "thesis of U. Bhagole)."
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of concrete fine collection.

        The fines are the cement fraction of the concrete waste, so about 7.27 t
        of concrete waste give one ton of fines.
        """
        li_dataset = CircularityDemandReductionConcreteLi(source_path=self.source_path)
        waste = li_dataset.get_concrete_per_cement()
        attr = self.conversion_factor
        attr.set_data(
            default_value=[
                {
                    "concrete_waste": {
                        "default_value": waste,
                        "unit": "tproduct/tproduct",
                    }
                },
                {
                    "electricity": {
                        "default_value": 0.00171 / 1000,
                        "unit": "GWh/tproduct",
                    }
                },
            ],
            source=AssumptionInformation(
                description=(
                    f"The fines are the cement fraction of the concrete waste: "
                    f"{waste:.2f} t of concrete waste per t of fines (inverse of the "
                    "cement content of 330 kg/m3 in 2400 kg/m3 concrete, Li 2003 and "
                    "Crista 2024). Electricity of 0.00171 MWh per t of fines, "
                    "assumption (model input of the MSc thesis of U. Bhagole)."
                ),
            ),
        )
        return attr

    def _set_capex_specific_conversion(self) -> Attribute:
        """
        Sets the specific capex of concrete fine collection.

        """
        attr = self.capex_specific_conversion
        attr.set_data(
            default_value=110000,
            unit="Euro/(tproduct/h)",
            source=AssumptionInformation(
                description=(
                    "Specific capex of 110000 Euro per (t fines/h), assumption "
                    "(model input of the MSc thesis of U. Bhagole)."
                ),
            ),
        )
        return attr

    def _set_opex_specific_variable(self) -> Attribute:
        """
        Sets the specific variable opex of concrete fine collection.

        """
        attr = self.opex_specific_variable
        attr.set_data(
            default_value=15,
            unit="Euro/tproduct",
            source=AssumptionInformation(
                description=(
                    "Variable opex of 15 Euro per t fines, assumption (model input "
                    "of the MSc thesis of U. Bhagole)."
                ),
            ),
        )
        return attr
