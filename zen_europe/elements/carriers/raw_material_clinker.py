# demandreductioncircularity: new carrier raw_material_clinker
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation
from zen_creator.elements import Carrier
from zen_creator.utils.attribute import Attribute


class RawMaterialClinker(Carrier):
    """Raw material for clinker carrier class.

    Virgin raw material for clinker production (limestone, clay, shale),
    converted into clinker input material by raw_material_for_clinker.
    """

    name: str = "raw_material_clinker"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_availability_import(self) -> Attribute:
        """
        Return the import availability of raw material for clinker.

        """
        attr = self.availability_import
        attr.set_data(
            default_value=np.inf,
            unit=self.power_unit,
            source=AssumptionInformation(
                description=(
                    "Raw material for clinker (limestone, clay, shale) is available without limits."
                ),
            ),
        )
        return attr

    # price_import keeps the zen-creator default of 0 (no raw material cost).
