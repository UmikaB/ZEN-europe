# demandreductioncircularity: new carrier train_mileage (intermediate)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier
from zen_creator.utils.attribute import Attribute


class TrainMileage(Carrier):
    """TrainMileage carrier class.

    Passenger-km delivered by regional trains. Converted 1:1 into urban or
    regional passenger transport by a dummy technology.
    """

    name: str = "train_mileage"

    def __init__(self, model: Model, power_unit: str = "pkm/h"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_availability_import(self) -> Attribute:
        """
        Return the availability of import of the carrier (none).

        """
        return Attribute(
            "availability_import",
            default_value=0,
            element=self,
            unit="pkm/h",
        )
