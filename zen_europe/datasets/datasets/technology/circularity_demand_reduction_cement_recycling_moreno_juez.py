# demandreductioncircularity: new dataset, electricity of cement recycling
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionCementRecyclingMorenoJuez(Dataset[pd.Series]):
    """
    Dataset class for the electricity use of recovering unhydrated cement.
    """

    name = "circularity_demand_reduction_cement_recycling_moreno_juez"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Treatment of end-of-life concrete in an innovative heating-air "
                "classification system for circular cement-based products"
            ),
            author=[
                "J. Moreno-Juez",
                "I. J. Vegas",
                "A. T. Gebremariam",
                "V. García-Cortés",
                "F. Di Maio",
            ],
            publication="Journal of Cleaner Production, vol. 263, 121515",
            publication_year=2020,
            url="https://doi.org/10.1016/j.jclepro.2020.121515",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            # MWh electricity per t recovered cement
            {"electricity": 0.040},
            name="conversion_factor",
        )

    # -------- methods ------------------------

    def get_electricity_per_cement(self) -> float:
        """
        Get the electricity use of cement recycling, in GWh per t cement.
        """
        return float(self.data["electricity"]) / 1000
