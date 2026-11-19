# demandreductioncircularity: new dataset, hourly profile of passenger travel
from __future__ import annotations

import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionPassengerTransportProfileMedvid(Dataset[pd.DataFrame]):
    """
    Dataset class for the hourly profile of urban and regional passenger
    transport.

    A weekday and a weekend shape of 24 hours, with morning and evening peaks
    on weekdays and a midday and an evening bump on weekends, repeated over the
    year (five weekdays, two weekend days). Both shapes have the same daily
    total. The shapes are based on empirical studies of public transport usage
    (Medvid et al. 2020) and of peak-period travel of private cars (Wemegah et al. 2018);
    the exact hourly values are not taken from a table in these studies.
    """

    name = "circularity_demand_reduction_passenger_transport_profile_medvid"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Occupancy of Public Transport Vehicles in Slovakia",
            author=["P. Medvid", "M. Gogola", "S. Kubalak"],
            publication="Transportation Research Procedia, vol. 44, pp. 153-159",
            publication_year=2020,
            url="https://doi.org/10.1016/j.trpro.2020.02.022",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.DataFrame:
        weekday = np.array(
            [0.5, 0.4, 0.3, 0.2, 0.3, 0.6, 1.0, 1.2, 1.1, 0.9, 0.8, 0.7]
            + [0.6, 0.6, 0.7, 0.8, 0.9, 1.1, 1.3, 1.0, 0.7, 0.5, 0.4, 0.3]
        )
        weekend = np.ones(24) * 0.5
        weekend[11:14] = 1.0  # midday bump
        weekend[17:19] = 0.7  # evening bump
        return pd.DataFrame(
            {"weekday": weekday / weekday.mean(), "weekend": weekend / weekend.mean()}
        )

    # -------- methods ------------------------

    def get_profile(self, year: int, nodes: list[str]) -> pd.DataFrame:
        """
        Get the hourly profile of one year, normalized to an annual sum of 1.

        Args:
            year: The calendar year that sets the weekdays and weekends.
            nodes: The nodes (columns).

        Returns:
            pd.DataFrame: 8760 hours x nodes, every column sums to 1.
        """
        days = pd.date_range(datetime.date(year, 1, 1), periods=365, freq="D")
        shape = np.concatenate(
            [
                (
                    self.data["weekend"].to_numpy()
                    if day.weekday() >= 5
                    else self.data["weekday"].to_numpy()
                )
                for day in days
            ]
        )
        shape = shape / shape.sum()
        profile = pd.DataFrame(
            np.outer(shape, np.ones(len(nodes))), columns=pd.Index(nodes)
        )
        profile.index.name = "time"
        return profile
