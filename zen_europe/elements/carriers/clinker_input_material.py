# demandreductioncircularity: new carrier clinker_input_material
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier


class ClinkerInputMaterial(Carrier):
    """Clinker input material carrier class.

    Raw material input of the cement kiln, from virgin raw material
    (raw_material_for_clinker) or concrete fines (cement_fines_for_clinker).
    """

    name: str = "clinker_input_material"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # Intermediate product without demand, import or export: all attributes keep
    # the zen-creator defaults (demand, availability_import and
    # availability_export 0).
