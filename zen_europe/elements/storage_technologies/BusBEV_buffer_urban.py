# demandreductioncircularity: new dummy storage BusBEV_buffer_urban
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, StorageTechnology

# assumptions of the thesis input
_LIFETIME = 100
_CAPEX_SPECIFIC_STORAGE = 1.0  # Euro per (pkm/h), a small cost
_EFFICIENCY = 0.999


class BusBEVBufferUrban(StorageTechnology):
    """Dummy storage of the bus_mileage of battery electric buses.

    The charging profile of the battery electric buses (max_load) does not
    follow the hourly profile of the passenger transport demand. This
    fictitious battery lets the passenger-km be stored in hours of low demand
    and released in hours of high demand, like storing electricity in the
    vehicle battery. Almost no cost and almost no losses.
    """

    name: str = "BusBEV_buffer_urban"

    def __init__(self, model: Model, power_unit: str = "megapkm/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier of the storage to bus_mileage.
        """
        return Attribute(
            name="reference_carrier", default_value=["bus_mileage"], element=self
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of the dummy storage.
        """
        attr = self.lifetime
        attr.set_data(
            default_value=_LIFETIME,
            source=AssumptionInformation(
                description=(
                    f"Dummy storage, lifetime of {_LIFETIME} years "
                ),
            ),
        )
        return attr

    def _set_capex_specific_storage(self) -> Attribute:
        """
        Sets the specific capex of the power capacity of the dummy storage.
        """
        attr = self.capex_specific_storage
        attr.set_data(
            default_value=_CAPEX_SPECIFIC_STORAGE,
            unit="Euro/(pkm/h)",
            source=AssumptionInformation(
                description=(
                    "Dummy storage with a small capex of "
                    f"{_CAPEX_SPECIFIC_STORAGE} Euro per (pkm/h)"
                ),
            ),
        )
        return attr

    def _set_efficiency_charge(self) -> Attribute:
        """
        Sets the charge efficiency of the dummy storage.
        """
        return self._set_efficiency(self.efficiency_charge)

    def _set_efficiency_discharge(self) -> Attribute:
        """
        Sets the discharge efficiency of the dummy storage.
        """
        return self._set_efficiency(self.efficiency_discharge)

    def _set_efficiency(self, attr: Attribute) -> Attribute:
        """Set an efficiency of the dummy storage to almost 1."""
        attr.set_data(
            default_value=_EFFICIENCY,
            unit="1",
            source=AssumptionInformation(
                description=(
                    f"Dummy storage with almost no losses, efficiency of "
                    f"{_EFFICIENCY} "
                ),
            ),
        )
        return attr
