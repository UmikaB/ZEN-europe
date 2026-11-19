# demandreductioncircularity: new dataset, train variable opex (Gleave 2015)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionTrainGleave(Dataset[pd.Series]):
    """
    Dataset class for the variable opex (excluding energy) of rail passenger
    transport, 0.024 Euro per passenger kilometre.
    """

    name = "circularity_demand_reduction_train_gleave"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Study on the Cost and Contribution of the Rail Sector",
            author=["Steer Davies Gleave"],
            publication="European Commission, DG MOVE",
            publication_year=2015,
            url=(
                "https://transport.ec.europa.eu/system/files/2016-09/2015-09-"
                "study-on-the-cost-and-contribution-of-the-rail-sector.pdf"
            ),
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        # variable opex in Euro per passenger km
        return pd.Series({"train": 0.024}, name="opex_variable_per_pkm")

    # -------- methods ------------------------

    def get_opex_variable_per_pkm(self, technology: str = "train") -> float:
        """Get the variable opex of a train in Euro per passenger kilometre."""
        return float(self.data[technology])
