# demandreductioncircularity: new carrier cement
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier


class Cement(Carrier):
    """Cement carrier class.

    Produced from clinker (clinker_to_cement) or recovered from concrete
    waste (cement_recycling), and used to make concrete (cement_to_concrete).
    """

    name: str = "cement"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # Intermediate product without demand, import or export: all attributes keep
    # the zen-creator defaults (demand, availability_import and
    # availability_export 0).
