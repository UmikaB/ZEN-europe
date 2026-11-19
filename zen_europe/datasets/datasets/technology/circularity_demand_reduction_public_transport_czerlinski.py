# demandreductioncircularity: new dataset, vehicle capacity (Czerlinski 2025)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionPublicTransportCzerlinski(Dataset[pd.Series]):
    """
    Dataset class for the maximum passenger capacity of buses and trams.

    The average occupancy is the maximum capacity times the occupancy rate
    """

    name = "circularity_demand_reduction_public_transport_czerlinski"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Capacity of Zero-Emission Urban Public Transport",
            author=["M. Czerlinski", "P. Pawlowski"],
            publication="Sustainability, vol. 17, no. 13, 5835",
            publication_year=2025,
            url="https://doi.org/10.3390/su17135835",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        # maximum capacity in passengers per vehicle
        return pd.Series(
            {
                "bus_ICE_diesel": 80.0,
                "bus_BEV": 80.0,
                "tram_metro": 200.0,
            },
            name="max_capacity",
        )

    # -------- methods ------------------------

    def get_max_capacity(self, technology: str) -> float:
        """Get the maximum number of passengers of one vehicle."""
        return float(self.data[technology])
