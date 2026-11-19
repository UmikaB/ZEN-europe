# demandreductioncircularity: new dataset collection, buses, trams/metros and trains
"""Techno-economic data of public transport (MSc thesis of U. Bhagole).

Rebuilds the values of thesis Tables 3.1 and 3.2 from their sources with the
formulas of thesis Appendix B.1:

- average occupancy = maximum capacity x occupancy rate (Eq. B.2)
- average speed = annual mileage / 8760 h (Table B.3)
- capex = (purchase cost / markup factor) / (occupancy x average speed) (Eq. B.1)
- variable opex per pkm = variable opex per vkm / occupancy (Eq. B.3)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, cast

if TYPE_CHECKING:
    from pathlib import Path

    from zen_creator import Dataset

from zen_creator import (
    AssumptionInformation,
    Attribute,
    ConversionTechnology,
    DatasetCollection,
    SourceInformation,
)
from zen_creator.datasets.datasets.metadata import MetadataTree

from zen_europe.datasets.datasets.technology.circularity_demand_reduction_bus_cooney import (
    CircularityDemandReductionBusCooney,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_bus_sistig import (
    CircularityDemandReductionBusSistig,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_public_transport_czerlinski import (
    CircularityDemandReductionPublicTransportCzerlinski,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_public_transport_eea import (
    CircularityDemandReductionPublicTransportEEA,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_public_transport_enerdata import (
    CircularityDemandReductionPublicTransportEnerdata,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_public_transport_miraftabzadeh import (
    CircularityDemandReductionPublicTransportMiraftabzadeh,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_train_bombardier import (
    CircularityDemandReductionTrainBombardier,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_train_gleave import (
    CircularityDemandReductionTrainGleave,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_train_thameslink import (
    CircularityDemandReductionTrainThameslink,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_tram_guerrieri import (
    CircularityDemandReductionTramGuerrieri,
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_tram_mondal import (
    CircularityDemandReductionTramMondal,
)
from zen_europe.utils.constants import Constants

# the share of the purchase price that is the conversion technology itself:
# 1/1.4, the same markup factor as for the passenger cars  of Cox et al. (2020)
MARKUP_FACTOR = 1.4
# assumed annual mileage per vehicle in km (thesis Table B.3)
ANNUAL_MILEAGE = {
    "bus_ICE_diesel": 70000.0,
    "bus_BEV": 70000.0,
    "tram_metro": 60000.0,
    "train": 200000.0,
}
# purchase cost of one tram in Euro as used in the thesis input (thesis Table
# B.1). The thesis cites Guerrieri (2019) [71], who gives 2.5-3.5 M Euro per
# tram, so 0.30 M Euro is probably a factor 10 too low (the thesis code marks it
# as a placeholder). Kept for now so that ZEN-europe reproduces the thesis; to
# use the source instead, take
# CircularityDemandReductionTramGuerrieri.get_purchase_cost() (3.0 M Euro).
TRAM_PURCHASE_COST_THESIS_INPUT = 0.30e6
# assumed lifetime of a regional train in years (thesis Table 3.2)
TRAIN_LIFETIME = 45

# dataset that reports each value, per technology
_ENERGY_SOURCE = {
    "bus_ICE_diesel": "enerdata",
    "train": "enerdata",
    "bus_BEV": "miraftabzadeh",
    "tram_metro": "miraftabzadeh",
}
_CAPACITY_SOURCE = {
    "bus_ICE_diesel": "czerlinski",
    "bus_BEV": "czerlinski",
    "tram_metro": "czerlinski",
    "train": "thameslink",
}
_INPUT_CARRIER = {
    "bus_ICE_diesel": "diesel",
    "bus_BEV": "electricity",
    "tram_metro": "electricity",
    "train": "electricity",
}


class CircularityDemandReductionPublicTransport(DatasetCollection):
    """Techno-economic data of buses, trams/metros and regional trains."""

    name = "circularity_demand_reduction_public_transport"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> Dict[str, Dataset[Any]]:
        """Load all available data sources."""

        if self.source_path is None:
            raise ValueError("source_path must be set to load the dataset collection.")

        return {
            "sistig": CircularityDemandReductionBusSistig(self.source_path),
            "czerlinski": CircularityDemandReductionPublicTransportCzerlinski(
                self.source_path
            ),
            "eea": CircularityDemandReductionPublicTransportEEA(self.source_path),
            "enerdata": CircularityDemandReductionPublicTransportEnerdata(
                self.source_path
            ),
            "miraftabzadeh": CircularityDemandReductionPublicTransportMiraftabzadeh(
                self.source_path
            ),
            "cooney": CircularityDemandReductionBusCooney(self.source_path),
            "guerrieri": CircularityDemandReductionTramGuerrieri(self.source_path),
            "mondal": CircularityDemandReductionTramMondal(self.source_path),
            "bombardier": CircularityDemandReductionTrainBombardier(self.source_path),
            "thameslink": CircularityDemandReductionTrainThameslink(self.source_path),
            "gleave": CircularityDemandReductionTrainGleave(self.source_path),
        }

    # -------- helpers ------------------

    def _metadata(self, *names: str) -> Dict[str, MetadataTree]:
        """Metadata of some of the datasets of the collection."""
        return {name: self.data[name].metadata for name in names}

    def get_occupancy(self, technology: str) -> float:
        """Average number of passengers per vehicle (thesis Eq. B.2)."""
        capacity = cast(Any, self.data[_CAPACITY_SOURCE[technology]])
        rate = cast(Any, self.data["eea"]).get_occupancy_rate(technology)
        return float(capacity.get_max_capacity(technology) * rate)

    @staticmethod
    def get_average_speed(technology: str) -> float:
        """Utilisation-based average speed in km/h (thesis Table B.3)."""
        return ANNUAL_MILEAGE[technology] / Constants.HOURS_PER_YEAR

    def get_purchase_cost(self, technology: str) -> tuple[float, str]:
        """Purchase cost of one vehicle in Euro, and the dataset it is from."""
        if technology in ("bus_ICE_diesel", "bus_BEV"):
            sistig = cast(CircularityDemandReductionBusSistig, self.data["sistig"])
            return sistig.get_purchase_cost(technology), "sistig"
        if technology == "tram_metro":
            return TRAM_PURCHASE_COST_THESIS_INPUT, "guerrieri"
        if technology == "train":
            bombardier = cast(
                CircularityDemandReductionTrainBombardier, self.data["bombardier"]
            )
            return bombardier.get_purchase_cost(), "bombardier"
        raise ValueError(f"No purchase cost for '{technology}'.")

    # -------- attribute setters ------------------

    def get_conversion_factor(self, element: ConversionTechnology) -> Attribute:
        """Energy use per passenger-km (thesis Table 3.1)."""
        source_name = _ENERGY_SOURCE[element.name]
        energy = cast(Any, self.data[source_name]).get_energy_per_pkm(element.name)
        carrier = _INPUT_CARRIER[element.name]
        attr = element.conversion_factor
        return attr.set_data(
            default_value=[{carrier: {"default_value": energy, "unit": "GWh/pkm"}}],
            source=SourceInformation(
                description=(
                    f"{carrier.capitalize()} use of {element.name} per "
                    f"passenger-km, {energy * 1e3:.3e} MWh/pkm "
                    " Values per vehicle-km are converted with the average occupancy."
                ),
                metadata=self._metadata(source_name),
            ),
        )

    def get_capex_specific_conversion(self, element: ConversionTechnology) -> Attribute:
        """Capex per unit of capacity (thesis Eq. B.1)."""
        purchase_cost, cost_source = self.get_purchase_cost(element.name)
        occupancy = self.get_occupancy(element.name)
        speed = self.get_average_speed(element.name)
        capex = purchase_cost / MARKUP_FACTOR / (occupancy * speed)
        description = (
            f"Capex of {element.name}: purchase cost of {purchase_cost / 1e6:.2f} "
            f"M Euro per vehicle, divided by the markup factor {MARKUP_FACTOR} "
            f"and by the capacity of one vehicle, i.e. its average occupancy "
            f"({occupancy:.0f} passengers) times its utilisation-based average "
            f"speed ({ANNUAL_MILEAGE[element.name]:.0f} km per year / 8760 h = "
            f"{speed:.2f} km/h)."
        )
        if element.name == "tram_metro":
            description += (
                " The tram purchase cost of 0.30 M Euro is the value of the thesis "
                "input (Table B.1). Its source, Guerrieri (2019), gives 2.5-3.5 M "
                "Euro per tram, so the value is probably a factor 10 too low; it "
                "is kept to reproduce the thesis."
            )
        attr = element.capex_specific_conversion
        attr.set_data(
            default_value=capex,
            unit="Euro/(pkm/h)",
            source=SourceInformation(
                description=description,
                metadata=self._metadata(
                    cost_source,
                    _CAPACITY_SOURCE[element.name],
                    "eea",
                ),
            ),
        )
        attr.add_source(
            AssumptionInformation(
                description=(
                    f"Annual mileage of {ANNUAL_MILEAGE[element.name]:.0f} km per "
                    f"vehicle and markup factor of {MARKUP_FACTOR}  "
                )
            )
        )
        return attr

    def get_opex_specific_variable(self, element: ConversionTechnology) -> Attribute:
        """Variable opex excluding energy per passenger-km (thesis Eq. B.3)."""
        attr = element.opex_specific_variable
        if element.name in ("bus_ICE_diesel", "bus_BEV"):
            sistig = cast(CircularityDemandReductionBusSistig, self.data["sistig"])
            occupancy = self.get_occupancy(element.name)
            value = sistig.get_opex_variable_per_vkm(element.name) / occupancy
            description = (
                f"Variable opex of {element.name}: "
                f"{sistig.get_opex_variable_per_vkm(element.name):.3f} Euro per "
                f"vehicle-km divided by the average occupancy of {occupancy:.0f} passengers."
            )
            names: tuple[str, ...] = ("sistig", "czerlinski", "eea")
        elif element.name == "tram_metro":
            sistig = cast(CircularityDemandReductionBusSistig, self.data["sistig"])
            value = sistig.get_opex_variable_per_pkm(element.name)
            description = (
                "Variable opex of tram_metro " #todo; roughly based on the source but check if a better source is available
            )
            names = ("sistig",)
        else:
            gleave = cast(CircularityDemandReductionTrainGleave, self.data["gleave"])
            value = gleave.get_opex_variable_per_pkm()
            description = (
                "Variable opex of a regional train per passenger-km "
            )
            names = ("gleave",)
        return attr.set_data(
            default_value=value,
            unit="Euro/pkm",
            source=SourceInformation(
                description=description, metadata=self._metadata(*names)
            ),
        )

    def get_opex_specific_fixed(self, element: ConversionTechnology) -> Attribute:
        """Fixed opex per unit of capacity and year (thesis Table 3.2)."""
        sistig = cast(CircularityDemandReductionBusSistig, self.data["sistig"])
        value = sistig.get_opex_fixed(element.name)
        description = (
            f"Fixed opex of {element.name}, {value} Euro per (pkm/h) and year "
        )
        attr = element.opex_specific_fixed
        return attr.set_data(
            default_value=value,
            unit="Euro/(pkm/h)",
            source=SourceInformation(
                description=(
                    f"Fixed opex of {element.name}, {value} Euro per (pkm/h) and year."
                ),
                metadata=self._metadata("sistig"),
            ),
        )

    def get_lifetime(self, element: ConversionTechnology) -> Attribute:
        """Lifetime in years (thesis Table 3.2)."""
        attr = element.lifetime
        if element.name in ("bus_ICE_diesel", "bus_BEV"):
            value = cast(CircularityDemandReductionBusCooney, self.data["cooney"])
            return attr.set_data(
                default_value=value.get_lifetime(element.name),
                unit="1",
                source=SourceInformation(
                    description=f"Lifetime of {element.name}.",
                    metadata=self._metadata("cooney"),
                ),
            )
        if element.name == "tram_metro":
            value_tram = cast(CircularityDemandReductionTramMondal, self.data["mondal"])
            return attr.set_data(
                default_value=value_tram.get_lifetime(element.name),
                unit="1",
                source=SourceInformation(
                    description="Lifetime of trams and metros.",
                    metadata=self._metadata("mondal"),
                ),
            )
        return attr.set_data(
            default_value=TRAIN_LIFETIME,
            unit="1",
            source=AssumptionInformation(
                description=(
                    f"Lifetime of a regional train of {TRAIN_LIFETIME} years (assumption) "
                )
            ),
        )
