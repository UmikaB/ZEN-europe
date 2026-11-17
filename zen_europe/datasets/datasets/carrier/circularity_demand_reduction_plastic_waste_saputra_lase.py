# demandreductioncircularity: new dataset, improved plastic recycling shares
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionPlasticWasteSaputraLase(Dataset[pd.Series]):
    """
    Dataset class for the improved recycling shares of post-consumer plastic
    waste.

    In line with the JRC "Improved scenario", 65% of post-consumer plastic
    waste is recycled: 46% through mechanical recycling and 19% through
    chemical recycling. Used as minimum shares in the industrial circular push
    scenario of the MSc thesis of U. Bhagole.
    """

    name = "circularity_demand_reduction_plastic_waste_saputra_lase"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "How much can chemical recycling contribute to plastic waste "
                "recycling in Europe? An assessment using material flow analysis "
                "modeling"
            ),
            author=[
                "I. Saputra Lase",
                "D. Tonini",
                "D. Caro",
                "P. F. Albizzati",
                "J. Cristobal Garcia",
                "M. Roosen",
                "M. Kusenberg",
                "K. Ragaert",
                "K. M. Van Geem",
                "J. Dewulf",
                "S. De Meester",
            ],
            publication="Resources, Conservation and Recycling, vol. 192, 106916",
            publication_year=2023,
            url="https://doi.org/10.1016/j.resconrec.2023.106916",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            {
                "mechanical_recycling_plastic": 0.46,
                "chemical_recycling_plastic": 0.19,
            },
            name="recycling_share",
        )

    # -------- methods ------------------------

    def get_recycling_share(self, technology: str) -> float:
        """
        Get the share of plastic waste treated by a recycling technology in the
        improved scenario.
        """
        return float(self.data[technology])
