# demandreductioncircularity: new dataset, car trips below 100 km (Rich & Mabit)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionPassengerTransportRichMabit(Dataset[pd.Series]):
    """
    Dataset class for the split of car passenger-km into urban and regional
    transport.

    About half of all European car passenger-km occur on trips shorter than
    100 km (Rich & Mabit 2012). Urban passenger transport therefore includes
    50% of the car passenger-km, regional passenger transport the other 50%.
    """

    name = "circularity_demand_reduction_passenger_transport_rich_mabit"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="A long-distance travel demand model for Europe",
            author=["J. Rich", "S. L. Mabit"],
            publication=(
                "European Journal of Transport and Infrastructure Research, "
                "vol. 12, no. 1"
            ),
            publication_year=2012,
            url="https://doi.org/10.18757/ejtir.2012.12.1.2946",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        # share of the car passenger-km on trips shorter than 100 km
        return pd.Series({"urban": 0.5, "regional": 0.5}, name="car_share")

    # -------- methods ------------------------

    def get_car_share(self, transport_type: str) -> float:
        """Get the share of the car passenger-km in 'urban' or 'regional'."""
        return float(self.data[transport_type])
