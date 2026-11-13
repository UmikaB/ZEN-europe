# demandreductioncircularity: new dataset, electricity of concrete production
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionCementToConcreteMPA(Dataset[pd.Series]):
    """
    Dataset class for the electricity use of ready-mixed concrete production.

    The sector EPD of the Mineral Products Association gives about 0.00131 MWh
    of electricity per ton of ready-mixed concrete.
    """

    name = "circularity_demand_reduction_cement_to_concrete_mpa"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Environmental Product Declaration for Ready-mixed concrete C28/35 "
                "CIIIA+SR Sector EPD"
            ),
            author=["Mineral Products Association (MPA) UK"],
            publication="Tech. Rep., MPA UK",
            publication_year=2024,
            url=(
                "https://www.sustainableconcrete.org.uk/Sustainable/media/"
                "Sustainable/Publications/C28-35-CIIIA-SR-ready-mixed-concrete.pdf"
            ),
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            # MWh electricity per t concrete
            {"electricity": 0.00131},
            name="conversion_factor",
        )

    # -------- methods ------------------------

    def get_electricity_per_concrete(self) -> float:
        """
        Get the electricity use of concrete production, in GWh per t concrete.
        """
        return float(self.data["electricity"]) / 1000
