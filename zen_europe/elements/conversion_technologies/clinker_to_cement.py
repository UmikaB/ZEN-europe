# demandreductioncircularity: new technology clinker -> cement
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology, Scenario

from zen_europe.datasets.datasets.carrier.aidres import Aidres
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    CLINKER_TO_CEMENT_CLINKER_FACTOR,
    EFFICIENCY_IMPROVEMENTS,
    scale_conversion_factor,
)


class ClinkerToCement(ConversionTechnology):
    """Dummy technology for blending clinker into CEM II cement.

    It sets the clinker-to-cement ratio. Costs and electricity of the whole cement plant, including
    cement grinding, are in the cement kiln.
    """

    name: str = "clinker_to_cement"

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
        Sets the input carrier to clinker. No electricity: it is in the cement
        kiln.
        """
        return Attribute(
            name="input_carrier",
            default_value=["clinker"],
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
        Sets the lifetime of clinker to cement.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=20,
            source=AssumptionInformation(
                description=(
                    "Lifetime of 20 years, assumption (MSc thesis U. Bhagole, "
                    "Table 3.4)."
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of clinker to cement.

        Efficiency improvements: clinker-to-cement ratio from 0.70 to 0.50, only
        the clinker input changes.
        """
        aidres_dataset = Aidres(source_path=self.source_path)
        attr = aidres_dataset.get_conversion_factor_clinker_to_cement(self)
        attr.add_scenarios(
            Scenario(
                EFFICIENCY_IMPROVEMENTS,
                default_value=scale_conversion_factor(
                    attr.default_value, {"clinker": CLINKER_TO_CEMENT_CLINKER_FACTOR}
                ),
            )
        )
        return attr

    def _set_capex_specific_conversion(self) -> Attribute:
        """
        Sets the specific capex of clinker to cement to 0.

        """
        attr = self.capex_specific_conversion
        attr.set_data(
            default_value=0,
            unit="Euro/(tproduct/h)",
            source=AssumptionInformation(
                description=(
                    "No separate capex: the capex of the cement kiln "
                    "(Gardarsdottir et al. 2019) covers the whole cement plant "
                    "including cement grinding, so a capex here would count the "
                    "grinding twice."
                ),
            ),
        )
        return attr
