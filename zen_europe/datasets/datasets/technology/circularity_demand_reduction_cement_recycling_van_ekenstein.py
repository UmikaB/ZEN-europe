# demandreductioncircularity: new dataset, concrete waste input of cement recycling
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionCementRecyclingVanEkenstein(Dataset[pd.Series]):
    """
    Dataset class for the concrete waste input of recovering unhydrated cement.
    """

    name = "circularity_demand_reduction_cement_recycling_van_ekenstein"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Downstream processing of End-of-Life concrete for the recovery of "
                "high-quality cementitious fractions"
            ),
            author=["A. A. Van Ekenstein", "H. Jonkers", "M. Ottelé"],
            publication="Cement, vol. 18, 100121",
            publication_year=2024,
            url="https://doi.org/10.1016/j.cement.2024.100121",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            # t concrete waste per t recovered cement
            {"concrete_waste": 1.0},
            name="conversion_factor",
        )

    # -------- methods ------------------------

    def get_concrete_waste_per_cement(self) -> float:
        """
        Get the concrete waste input of cement recycling, in t per t cement.
        """
        return float(self.data["concrete_waste"])
