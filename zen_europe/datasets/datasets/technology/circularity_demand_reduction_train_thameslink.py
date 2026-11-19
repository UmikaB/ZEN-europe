# demandreductioncircularity: new dataset, train capacity (First Capital Connect 2013)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionTrainThameslink(Dataset[pd.Series]):
    """
    Dataset class for the passenger capacity of a medium-capacity train.

    The Thameslink Class 700 train (8 cars) carries 1182 passengers. The
    average occupancy is the maximum capacity times the occupancy rate
    """

    name = "circularity_demand_reduction_train_thameslink"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "First Capital Connect and Siemens reveal further details of "
                "Thameslink train order"
            ),
            author=["First Capital Connect"],
            publication="First Capital Connect, Media centre - News",
            publication_year=2013,
            url=(
                "https://web.archive.org/web/20131108012449/http://www."
                "firstcapitalconnect.co.uk/about-us/media-centre/news/2013/"
                "first-capital-connect-and-siemens-reveal-further-details-"
                "thameslink-train-order/"
            ),
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        # maximum capacity in passengers per train
        return pd.Series({"train": 1182.0}, name="max_capacity")

    # -------- methods ------------------------

    def get_max_capacity(self, technology: str) -> float:
        """Get the maximum number of passengers of one train."""
        return float(self.data[technology])
