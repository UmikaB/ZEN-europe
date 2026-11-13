# demandreductioncircularity: new carrier concrete
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier


class Concrete(Carrier):
    """Concrete carrier class.

    Produced from cement (cement_to_concrete) and split into concrete use
    and concrete waste (concrete_demolishment_overproduction).
    """

    name: str = "concrete"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # Intermediate product without demand, import or export: all attributes keep
    # the zen-creator defaults (demand, availability_import and
    # availability_export 0).
