# demandreductioncircularity: new carrier plastic
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier


class Plastic(Carrier):
    """Plastic carrier class.

    Produced by polymerisation and mechanical_recycling_plastic, and split into
    plastic use and plastic waste by overproduction_use_plastic.
    """

    name: str = "plastic"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # Intermediate product without demand, import or export: all attributes keep
    # the zen-creator defaults (demand, availability_import and
    # availability_export 0).
