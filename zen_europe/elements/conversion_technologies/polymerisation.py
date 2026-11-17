# demandreductioncircularity: new technology olefin -> plastic
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology, Scenario

from zen_europe.datasets.datasets.carrier.aidres import Aidres
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    EFFICIENCY_IMPROVEMENTS,
    POLYMERISATION_ENERGY_FACTOR,
    scale_conversion_factor,
)


class Polymerisation(ConversionTechnology):
    """Primary plastic production from olefins."""

    name: str = "polymerisation"

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
        Sets the input carriers to olefin, electricity and heat.
        """
        return Attribute(
            name="input_carrier",
            default_value=["olefin", "electricity", "heat"],
            element=self,
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carrier to plastic.
        """
        return Attribute(name="output_carrier", default_value=["plastic"], element=self)

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of polymerisation.

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
        Return the conversion factor of polymerisation.

        Efficiency improvements: electricity and heat x0.85 (process energy
        efficiency); olefin stays 1 t/t to keep the mass balance.
        """
        aidres_dataset = Aidres(source_path=self.source_path)
        attr = aidres_dataset.get_conversion_factor_polymerisation(self)
        attr.add_scenarios(
            Scenario(
                EFFICIENCY_IMPROVEMENTS,
                default_value=scale_conversion_factor(
                    attr.default_value,
                    {
                        "electricity": POLYMERISATION_ENERGY_FACTOR,
                        "heat": POLYMERISATION_ENERGY_FACTOR,
                    },
                ),
            )
        )
        return attr

    def _set_capex_specific_conversion(self) -> Attribute:
        """
        Sets the specific capex of polymerisation.

        """
        aidres_dataset = Aidres(source_path=self.source_path)
        return aidres_dataset.get_capex_specific_polymerisation(self)
