# demandreductioncircularity: new technology bus_BEV (battery electric buses)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import (
    AssumptionInformation,
    Attribute,
    ConversionTechnology,
    Scenario,
    SourceInformation,
)

from zen_europe.datasets.dataset_collections.circularity_demand_reduction_public_transport import (
    CircularityDemandReductionPublicTransport,
)
from zen_europe.datasets.dataset_collections.existing_vehicle_capacity import (
    ExistingVehicleCapacity,
)
from zen_europe.datasets.dataset_collections.passenger_mileage_demand import (
    PassengerMileageDemand,
)
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    EFFICIENCY_IMPROVEMENTS,
    TRANSPORT_EFFICIENCY_FACTORS,
    scale_conversion_factor,
)


class Bus_BEV(ConversionTechnology):
    """Class containing all data and assumptions for battery electric buses"""

    name: str = "bus_BEV"

    def __init__(self, model: Model, power_unit: str = "megapkm/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier of bus_BEV to bus_mileage.
        """
        return Attribute(
            name="reference_carrier", default_value=["bus_mileage"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carrier of bus_BEV to electricity.
        """
        return Attribute(
            name="input_carrier", default_value=["electricity"], element=self
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Set the output carrier of bus_BEV to bus_mileage.
        """
        return Attribute(
            name="output_carrier", default_value=["bus_mileage"], element=self
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of bus_BEV.

        """
        public_transport = CircularityDemandReductionPublicTransport(self.source_path)
        return public_transport.get_lifetime(element=self)

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of bus_BEV, with the efficiency improvements
        scenario

        """
        public_transport = CircularityDemandReductionPublicTransport(self.source_path)
        attr = public_transport.get_conversion_factor(element=self)
        attr.add_scenarios(
            Scenario(
                EFFICIENCY_IMPROVEMENTS,
                default_value=scale_conversion_factor(
                    attr.default_value,
                    {"electricity": TRANSPORT_EFFICIENCY_FACTORS[self.name]},
                ),
            )
        )
        return attr

    def _set_capex_specific_conversion(self) -> Attribute:
        """
        Sets the specific conversion CAPEX of bus_BEV.

        """
        public_transport = CircularityDemandReductionPublicTransport(self.source_path)
        return public_transport.get_capex_specific_conversion(element=self)

    def _set_opex_specific_variable(self) -> Attribute:
        """
        Sets the specific variable OPEX of bus_BEV.

        """
        public_transport = CircularityDemandReductionPublicTransport(self.source_path)
        return public_transport.get_opex_specific_variable(element=self)

    def _set_opex_specific_fixed(self) -> Attribute:
        """
        Sets the specific fixed OPEX of bus_BEV.

        """
        public_transport = CircularityDemandReductionPublicTransport(self.source_path)
        return public_transport.get_opex_specific_fixed(element=self)

    def _set_capacity_existing(self) -> Attribute:
        """
        Sets the existing capacity of bus_BEV (UNECE bus registrations).

        """
        attr = self.capacity_existing
        if self.settings.investment.use_existing_capacities:
            vehicle_capacity = ExistingVehicleCapacity(
                settings=self.model.settings, source_path=self.source_path
            )
            ex_cap = vehicle_capacity.get_existing_capacity_bus(element=self)
            return attr.set_data(
                df=ex_cap,
                source=SourceInformation(
                    description=(
                        "The existing capacity of bus_BEV is calculated from the "
                        "new bus registrations of the UNECE dataset, the average "
                        "mileage of one bus (bus passenger-km of the Statistical "
                        "Pocketbook divided by the bus fleet) and the peak demand "
                        "share of the charging profile "
                    ),
                    metadata=vehicle_capacity.metadata,
                ),
                unit="megapkm/h",
            )
        attr.set_data(
            default_value=0,
            df=None,
            source=AssumptionInformation(
                description=("We do not consider existing capacities."),
            ),
        )
        return attr

    def _set_max_load(self) -> Attribute:
        """
        Sets the maximum load of bus_BEV to the charging profile of the cars
        (bus BEV profile = car profile scaled to the bus passenger-km).

        """
        passenger_transport_db = PassengerMileageDemand(
            settings=self.model.settings, source_path=self.source_path
        )
        return passenger_transport_db.get_max_load(element=self)
