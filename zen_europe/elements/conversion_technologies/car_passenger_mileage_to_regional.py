# demandreductioncircularity: new dummy technology, cars -> regional transport
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import AssumptionInformation, Attribute, ConversionTechnology


class CarPassengerMileageToRegional(ConversionTechnology):
    """Dummy technology that converts passenger_mileage 1:1 into
    regional_transport, without cost or losses.
    """

    name: str = "car_passenger_mileage_to_regional"

    def __init__(self, model: Model, power_unit: str = "megapkm/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier to regional_transport.
        """
        return Attribute(
            name="reference_carrier", default_value=["regional_transport"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carrier to passenger_mileage.
        """
        return Attribute(
            name="input_carrier", default_value=["passenger_mileage"], element=self
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Sets the output carrier to regional_transport.
        """
        return Attribute(
            name="output_carrier", default_value=["regional_transport"], element=self
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of the dummy technology.

        """
        attr = self.lifetime
        attr.set_data(
            default_value=100,
            source=AssumptionInformation(
                description=(
                    "Dummy technology, lifetime of 100 years (MSc thesis U. "
                    "Bhagole, thesis input)."
                ),
            ),
        )
        return attr

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor: 1 pkm of passenger_mileage per pkm of
        regional_transport.

        """
        attr = self.conversion_factor
        attr.set_data(
            default_value=[
                {"passenger_mileage": {"default_value": 1.0, "unit": "pkm/pkm"}}
            ],
            source=AssumptionInformation(
                description=(
                    "Dummy technology without losses "
                ),
            ),
        )
        return attr

    def _set_capex_specific_conversion(self) -> Attribute:
        """
        Sets the specific capex of the dummy technology to 0.

        """
        attr = self.capex_specific_conversion
        attr.set_data(
            default_value=0,
            unit="Euro/(pkm/h)",
            source=AssumptionInformation(
                description=(
                    "Dummy technology without cost"
                ),
            ),
        )
        return attr
