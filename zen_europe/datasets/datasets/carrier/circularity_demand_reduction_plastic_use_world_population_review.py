# demandreductioncircularity: new dataset, plastic consumption per country
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData

from zen_europe.utils.constants import Constants


class CircularityDemandReductionPlasticUseWorldPopulationReview(Dataset[pd.Series]):
    """
    Dataset class for the yearly plastic consumption per country.

    Reads the raw file Original_Plastic_Consumption__tons_year_.csv (t/y per
    country), compiled from World Population Review. Used as base-year final
    plastic demand.
    """

    name = "circularity_demand_reduction_plastic_use_world_population_review"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Plastic Pollution by Country 2025",
            author=["World Population Review"],
            publication="World Population Review",
            publication_year=2025,
            url=(
                "https://worldpopulationreview.com/country-rankings/"
                "plastic-pollution-by-country"
            ),
        )

    def _set_path(self) -> Path | None:
        if self.source_path is None:
            raise ValueError("source_path must be set to load the dataset.")
        return self.source_path / "02-carrier" / "industry"

    def _set_data(self) -> pd.Series:
        df = pd.read_csv(
            self.path / "Original_Plastic_Consumption__tons_year_.csv",
            index_col="node",
        )
        return df["plastic_consumption_tons_per_year"]

    # -------- methods ------------------------

    def get_plastic_consumption(self, nodes: list[str]) -> pd.Series:
        """
        Get the plastic consumption per node in t/h.

        Nodes that are not in the raw file get 0, as in the MSc thesis.

        Args:
            nodes: The nodes of the model.

        Returns:
            pd.Series: Plastic consumption in t/h, indexed by node.
        """
        d = self.data.reindex(nodes).fillna(0.0)
        d = d / Constants.HOURS_PER_YEAR  # t/y -> t/h
        d.index.name = "node"
        d.name = "demand"
        return d
