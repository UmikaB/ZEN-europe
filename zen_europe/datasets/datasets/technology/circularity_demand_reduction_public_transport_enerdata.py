# demandreductioncircularity: new dataset, energy use per pkm (Enerdata, ODYSSEE-MURE)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionPublicTransportEnerdata(Dataset[pd.Series]):
    """
    Dataset class for the specific energy consumption of diesel buses and
    regional trains per passenger kilometre.

    The values are in MWh/pkm
    """

    name = "circularity_demand_reduction_public_transport_enerdata"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Specific energy consumption by transport mode | ODYSSEE-MURE",
            author=["Enerdata"],
            publication="ODYSSEE-MURE",
            publication_year=2024,
            url=(
                "https://www.odyssee-mure.eu/publications/efficiency-by-sector/"
                "transport/specific-consumption.html"
            ),
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        # energy use in MWh per passenger km
        return pd.Series(
            {"bus_ICE_diesel": 2.444e-4, "train": 7.0e-5},
            name="energy_per_pkm",
        )

    # -------- methods ------------------------

    def get_energy_per_pkm(self, technology: str) -> float:
        """Get the energy use in GWh per passenger kilometre."""
        return float(self.data[technology]) / 1000
