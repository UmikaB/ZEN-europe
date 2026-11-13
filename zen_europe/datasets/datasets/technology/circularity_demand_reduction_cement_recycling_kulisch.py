# demandreductioncircularity: new dataset, recoverable unhydrated cement (Kulisch 2022)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionCementRecyclingKulisch(Dataset[pd.Series]):
    """
    Dataset class for the share of concrete waste that can be recovered as
    unhydrated cement.

    6-36% of hardened concrete and paste can consist of unhydrated cement grains
    (Kulisch et al. 2022). The industrial circular push scenario allows at most
    the midpoint, 21%, of the concrete waste to be used by cement_recycling.
    """

    name = "circularity_demand_reduction_cement_recycling_kulisch"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Quantification of Residual Unhydrated Cement Content in Cement "
                "Pastes as a Potential for Recovery"
            ),
            author=["D. Kulisch", "A. Katz", "S. Zhutovsky"],
            publication="Sustainability, vol. 15, no. 1, 263",
            publication_year=2022,
            url="https://doi.org/10.3390/su15010263",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            # share of unhydrated cement in hardened concrete and paste
            {"unhydrated_share_min": 0.06, "unhydrated_share_max": 0.36},
            name="unhydrated_cement_share",
        )

    # -------- methods ------------------------

    def get_recoverable_share(self) -> float:
        """
        Get the share of concrete waste that can be recovered as unhydrated
        cement, the midpoint of 6-36%.
        """
        return float(
            (self.data["unhydrated_share_min"] + self.data["unhydrated_share_max"]) / 2
        )
