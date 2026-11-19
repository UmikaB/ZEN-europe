# demandreductioncircularity: new dataset, bus costs (Sistig et al. 2025)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionBusSistig(Dataset[pd.DataFrame]):
    """
    Dataset class for the costs of public buses from Sistig et al. (2025).

    Purchase cost per bus, fixed opex per unit of capacity and variable opex
    per vehicle kilometre (excluding energy), for diesel and battery electric
    buses. The variable opex is converted to Euro/pkm with the average bus
    occupancy.

    Same source used for the fixed opex of trams and trains and for the variable opex of
    trams.
    """

    name = "circularity_demand_reduction_bus_sistig"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Evaluating costs and operations of public bus fleet electrification",
            author=["H. M. Sistig", "P. Sinhuber", "M. Rogge", "D. U. Sauer"],
            publication="npj Sustainable Mobility and Transport, vol. 2, no. 1",
            publication_year=2025,
            url="https://doi.org/10.1038/s44333-025-00030-y",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                # purchase cost per vehicle, Euro (2019 values, thesis Table B.1)
                "purchase_cost": {"bus_ICE_diesel": 350000.0, "bus_BEV": 500000.0},
                # variable opex excluding energy, Euro per vehicle km
                # (thesis code: 0.00167 and 0.00208 Euro/pkm at 24 passengers)
                "opex_variable_per_vkm": {
                    "bus_ICE_diesel": 0.00167 * 24,
                    "bus_BEV": 0.00208 * 24,
                    "tram_metro": None,
                    "train": None,
                },
                # variable opex excluding energy, Euro per passenger km, as used
                # in the thesis for trams (Table 3.2; marked as a temporary
                # assumption in the thesis code)
                "opex_variable_per_pkm": {"tram_metro": 0.020},
                # fixed opex, Euro per (pkm/h) and year (thesis Table 3.2)
                "opex_fixed": {
                    "bus_ICE_diesel": 0.020,
                    "bus_BEV": 0.020,
                    "tram_metro": 0.020,
                    "train": 0.020,
                },
            }
        )

    # -------- methods ------------------------

    def get_purchase_cost(self, technology: str) -> float:
        """Get the purchase cost of one bus in Euro."""
        return float(self.data.loc[technology, "purchase_cost"])

    def get_opex_variable_per_vkm(self, technology: str) -> float:
        """Get the variable opex of a bus in Euro per vehicle kilometre."""
        return float(self.data.loc[technology, "opex_variable_per_vkm"])

    def get_opex_variable_per_pkm(self, technology: str) -> float:
        """Get the variable opex in Euro per passenger kilometre (trams)."""
        return float(self.data.loc[technology, "opex_variable_per_pkm"])

    def get_opex_fixed(self, technology: str) -> float:
        """Get the fixed opex in Euro per (pkm/h) and year."""
        return float(self.data.loc[technology, "opex_fixed"])
