# demandreductioncircularity: new dataset, growth of plastic consumption (OECD 2022)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionPlasticUseOECD(Dataset[pd.Series]):
    """
    Dataset class for the growth of plastic consumption.

    Following the OECD Global Plastics Outlook projections for Europe, plastic
    consumption doubles between the base year and 2060 (geometric growth).
    """

    name = "circularity_demand_reduction_plastic_use_oecd"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Global Plastics Outlook",
            author=["OECD"],
            publication="OECD Publishing, Paris",
            publication_year=2022,
            url="https://doi.org/10.1787/aa1edf33-en",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            # plastic consumption doubles (factor 2) by 2060
            {"growth_factor": 2.0, "target_year": 2060},
            name="plastic_growth",
        )

    # -------- methods ------------------------

    def get_yearly_variation(self, years: list[int], reference_year: int) -> pd.Series:
        """
        Get the yearly variation of plastic consumption relative to the
        reference year.

        Args:
            years: The model years.
            reference_year: The base year of the consumption data.

        Returns:
            pd.Series: Factor per year (1 in the reference year).
        """
        span = int(self.data["target_year"]) - reference_year
        growth_per_year = float(self.data["growth_factor"]) ** (1 / span)
        variation = pd.Series(
            {year: growth_per_year ** (year - reference_year) for year in years},
            name="demand_yearly_variation",
        )
        variation.index.name = "year"
        return variation
