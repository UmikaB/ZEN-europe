# demandreductioncircularity: new dataset, secondary steel trajectory (JRC 2021)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionScrapSteelJRC(Dataset[pd.Series]):
    """
    Dataset class for the secondary steel share trajectory of the JRC.

    Lower-bound JRC projection: secondary (scrap-based) steel production in
    Europe increases by 30% relative to 2018, so that the secondary steel share
    of total steel production rises from 39.7% in 2022 to 50% in 2050. The
    yearly values are stored in secondary_steel_share.xlsx (sheet
    share_secondary_steel, columns year and share_secondary).

    The trajectory is used for the scrap steel availability (together with the
    EAF scrap input, see CircularityDemandReductionEAFCappel) and for the
    demand share of secondary_steel_to_steel.
    """

    name = "circularity_demand_reduction_scrap_steel_jrc"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=("Decarbonisation of industrial heat: The iron and steel sector"),
            author=["Joint Research Centre (JRC)"],
            publication="JRC Technical Report JRC119415",
            publication_year=2021,
            url=(
                "https://setis.ec.europa.eu/system/files/2021-02/"
                "jrc119415_iron_and_steel_decarbonisation_brief.pdf"
            ),
        )

    def _set_path(self) -> Path | None:
        if self.source_path is None:
            raise ValueError("source_path must be set to load the dataset.")
        return self.source_path / "02-carrier" / "industry"

    def _set_data(self) -> pd.Series:
        df = pd.read_excel(
            self.path / "secondary_steel_share.xlsx",
            sheet_name="share_secondary_steel",
        )
        share = df.set_index("year")["share_secondary"].astype(float)
        share.index = share.index.astype(int)
        share.index.name = "year"
        share.name = "share_secondary"
        return share

    # -------- methods ------------------------

    def get_secondary_steel_share(self, years: list[int]) -> pd.Series:
        """
        Get the secondary steel share of total steel production per model year.

        Years between the values in the file are interpolated linearly.

        Args:
            years: The model years.

        Returns:
            pd.Series: The secondary steel share (0-1) indexed by year.
        """
        share = self.data
        missing = [y for y in years if y < share.index.min() or y > share.index.max()]
        if missing:
            raise ValueError(
                f"No secondary steel share for the years {missing} in "
                "secondary_steel_share.xlsx."
            )
        share = (
            share.reindex(sorted(set(share.index) | set(years)))
            .interpolate(method="index")
            .loc[years]
        )
        share.index.name = "year"
        return share.clip(0.0, 1.0)
