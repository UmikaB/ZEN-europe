# demandreductioncircularity: new dataset, tram lifetime (Mondal & Pohit 2025)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionTramMondal(Dataset[pd.Series]):
    """
    Dataset class for the lifetime of trams/metros (70 years).
    """

    name = "circularity_demand_reduction_tram_mondal"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Economics of trams versus alternative road-based urban transport "
                "mode: A life cycle cost analysis"
            ),
            author=["S. Mondal", "S. Pohit"],
            publication="ResearchGate preprint",
            publication_year=2025,
            url=(
                "https://www.researchgate.net/publication/390092116_Economics_of_"
                "Trams_versus_Alternative_Road-based_Urban_Transport_Mode_A_Life_"
                "Cycle_Cost_Analysis"
            ),
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        # lifetime in years
        return pd.Series({"tram_metro": 70}, name="lifetime")

    # -------- methods ------------------------

    def get_lifetime(self, technology: str) -> int:
        """Get the lifetime of a tram/metro in years."""
        return int(self.data[technology])
