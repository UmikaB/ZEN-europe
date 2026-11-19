# demandreductioncircularity: new dataset, tram purchase cost (Guerrieri 2019)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionTramGuerrieri(Dataset[pd.Series]):
    """
    Dataset class for the purchase cost of a tram vehicle.

    Guerrieri (2019) states that each tram vehicle costs 2.5-3.5 M Euro (about
    3.6 M Euro with on-board energy storage). The midpoint, 3.0 M Euro, is
    used. Todo: The thesis input used 0.30 M Euro (thesis Table B.1), which is a
    factor 10 below its own source --> requires check and then also the capex of other transport techs
    """

    name = "circularity_demand_reduction_tram_guerrieri"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Catenary-Free Tramway Systems: Functional and Cost-Benefit "
                "Analysis for a Metropolitan Area"
            ),
            author=["M. Guerrieri"],
            publication="Urban Rail Transit, vol. 5, no. 4, pp. 289-309",
            publication_year=2019,
            url="https://doi.org/10.1007/s40864-019-00118-y",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        # purchase cost per tram vehicle in Euro (range in the source)
        return pd.Series(
            {"purchase_cost_min": 2.5e6, "purchase_cost_max": 3.5e6},
            name="purchase_cost",
        )

    # -------- methods ------------------------

    def get_purchase_cost(self, technology: str = "tram_metro") -> float:
        """Get the purchase cost of one tram in Euro, the midpoint of the range."""
        return float(
            (self.data["purchase_cost_min"] + self.data["purchase_cost_max"]) / 2
        )
