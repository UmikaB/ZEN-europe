# demandreductioncircularity: new dataset, car occupancy (KBA)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Attribute
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionCarOccupancyKBA(Dataset[pd.Series]):
    """
    Dataset class for the average occupancy of passenger cars.

    Germany, about 18% of the European passenger mileage, reported 627.9
    billion vehicle-km (Kraftfahrt-Bundesamt, Inlaenderfahrleistung) and 902.6
    billion passenger-km (EU transport in figures, Statistical Pocketbook 2022,
    2019 value), so a car carries on average 902.6 / 627.9 = 1.44 passengers.
    The same occupancy is assumed for all countries. It converts the car data
    per vehicle-km to per passenger-km (the thesis code multiplies by
    627.949852 / 902.6).
    """

    name = "circularity_demand_reduction_car_occupancy_kba"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Inlaenderfahrleistung",
            author=["Kraftfahrt-Bundesamt (KBA)"],
            publication="KBA, Statistik, Verkehr in Kilometern",
            publication_year=2023,
            url=(
                "https://www.kba.de/DE/Statistik/Kraftverkehr/VerkehrKilometer/"
                "vk_inlaenderfahrleistung/vk_inlaenderfahrleistung_node.html"
            ),
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            {
                # vehicle km of passenger cars in Germany, billion (KBA)
                "vkm_DE": 627.949852,
                # passenger km of passenger cars in Germany, billion
                # (Statistical Pocketbook 2022, 2019)
                "pkm_DE": 902.6,
            },
            name="car_mileage",
        )

    # -------- methods ------------------------

    def get_occupancy(self) -> float:
        """Get the average number of passengers per car."""
        return float(self.data["pkm_DE"] / self.data["vkm_DE"])

    def convert_to_pkm(self, attr: Attribute) -> Attribute:
        """Convert an attribute of a passenger car from per vehicle-km to per
        passenger-km.

        Values per vehicle-km (conversion factor, variable opex) are divided
        by the occupancy and 'vkm' is replaced by 'pkm' in the unit.

        Args:
            attr: The attribute per vehicle-km.

        Returns:
            Attribute: The same attribute per passenger-km.
        """
        occupancy = self.get_occupancy()
        default_value = attr.default_value
        if isinstance(default_value, list):
            # conversion factor: [{carrier: {"default_value": ..., "unit": ...}}]
            attr.default_value = [
                {
                    carrier: {
                        **value,
                        "default_value": value["default_value"] / occupancy,
                        "unit": value["unit"].replace("vkm", "pkm"),
                    }
                    for carrier, value in entry.items()
                }
                for entry in default_value
            ]
        else:
            attr.default_value = float(default_value) / occupancy
            if attr.df is not None:
                attr.df = attr.df / occupancy
        if attr.unit is not None:
            attr.unit = attr.unit.replace("vkm", "pkm")
        attr.add_source(
            self.get_source_information(
                f"Converted from per vehicle-km to per passenger-km with an "
                f"average car occupancy of {occupancy:.3f} passengers (Germany, "
                "KBA vehicle-km and Statistical Pocketbook passenger-km), as in "
            )
        )
        return attr

    def get_source_information(self, description: str):
        """Return a SourceInformation with the metadata of this dataset."""
        from zen_creator import SourceInformation

        return SourceInformation(description=description, metadata=self.metadata)
