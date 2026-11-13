# demandreductioncircularity: new carrier concrete_fine
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier


class ConcreteFine(Carrier):
    """Concrete fine carrier class.

    Fines recovered from concrete waste (concrete_fine_collection), used as
    raw material for clinker (cement_fines_for_clinker).
    """

    name: str = "concrete_fine"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # Intermediate product without demand, import or export: all attributes keep
    # the zen-creator defaults (demand, availability_import and
    # availability_export 0).
