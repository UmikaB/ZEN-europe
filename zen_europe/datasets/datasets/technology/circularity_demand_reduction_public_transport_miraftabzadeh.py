# demandreductioncircularity: new dataset, energy per pkm (Miraftabzadeh 2024)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionPublicTransportMiraftabzadeh(Dataset[pd.Series]):
    """
    Dataset class for the electricity use of battery electric buses and
    trams/metros per passenger kilometre.

    Data in MWh/vkm converted to MWh/pkm with the average occupancy
    """

    name = "circularity_demand_reduction_public_transport_miraftabzadeh"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Comparative Analysis of Sustainable Electrification in "
                "Mediterranean Public Transportation"
            ),
            author=["S. M. Miraftabzadeh", "B. Ranjgar", "A. Niccolai", "M. Longo"],
            publication="Sustainability, vol. 16, no. 7, 2645",
            publication_year=2024,
            url="https://doi.org/10.3390/su16072645",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        # electricity use in MWh per passenger km
        return pd.Series(
            {"bus_BEV": 8.333e-5, "tram_metro": 9.0e-5},
            name="energy_per_pkm",
        )

    # -------- methods ------------------------

    def get_energy_per_pkm(self, technology: str) -> float:
        """Get the electricity use in GWh per passenger kilometre."""
        return float(self.data[technology]) / 1000
