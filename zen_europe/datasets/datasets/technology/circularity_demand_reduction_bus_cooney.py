# demandreductioncircularity: new dataset, bus lifetime (Cooney et al. 2013)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionBusCooney(Dataset[pd.Series]):
    """
    Dataset class for the lifetime of public buses (12 years), used for diesel
    and battery electric buses.
    """

    name = "circularity_demand_reduction_bus_cooney"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Life Cycle Assessment of Diesel and Electric Public "
                "Transportation Buses"
            ),
            author=["G. Cooney", "T. R. Hawkins", "J. Marriott"],
            publication="Journal of Industrial Ecology, vol. 17, no. 5, pp. 689-699",
            publication_year=2013,
            url="https://doi.org/10.1111/jiec.12024",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        # lifetime in years
        return pd.Series({"bus_ICE_diesel": 12, "bus_BEV": 12}, name="lifetime")

    # -------- methods ------------------------

    def get_lifetime(self, technology: str) -> int:
        """Get the lifetime of a bus in years."""
        return int(self.data[technology])
