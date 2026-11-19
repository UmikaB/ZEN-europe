# demandreductioncircularity: new dataset, occupancy rates (EEA)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionPublicTransportEEA(Dataset[pd.Series]):
    """
    Dataset class for the occupancy rates of buses, trams and trains.

    The average occupancy is the maximum capacity times the occupancy rate
    """

    name = "circularity_demand_reduction_public_transport_eea"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Occupancy rates",
            author=["European Environment Agency (EEA)"],
            publication="EEA, Environmental issues series no. 12",
            publication_year=1998,
            url="https://www.eea.europa.eu/publications/ENVISSUENo12/page029.html",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        # share of the maximum capacity that is occupied on average
        return pd.Series(
            {
                "bus_ICE_diesel": 0.30,
                "bus_BEV": 0.30,
                "tram_metro": 0.30,
                "train": 0.40,
            },
            name="occupancy_rate",
        )

    # -------- methods ------------------------

    def get_occupancy_rate(self, technology: str) -> float:
        """Get the average occupancy rate of a vehicle (0-1)."""
        return float(self.data[technology])
