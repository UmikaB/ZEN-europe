# demandreductioncircularity: new dataset, train purchase cost (Bombardier 2014)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionTrainBombardier(Dataset[pd.Series]):
    """
    Dataset class for the purchase cost of a regional train (5 M Euro), from
    the contract of Deutsche Bahn and Bombardier for 29 commuter trains.
    """

    name = "circularity_demand_reduction_train_bombardier"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Deutsche Bahn and Bombardier sign contract for 29 trains for "
                "commuter service in central Germany"
            ),
            author=["Bombardier Transportation"],
            publication="Mass Transit Magazine",
            publication_year=2014,
            url="https://www.masstransitmag.com/bombardier-29-trains",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        # purchase cost per train in Euro
        return pd.Series({"train": 5.0e6}, name="purchase_cost")

    # -------- methods ------------------------

    def get_purchase_cost(self, technology: str = "train") -> float:
        """Get the purchase cost of one train in Euro."""
        return float(self.data[technology])
