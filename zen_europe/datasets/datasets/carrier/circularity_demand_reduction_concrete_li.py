# demandreductioncircularity: new dataset, concrete composition (Li 2003, Crista 2024)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData


class CircularityDemandReductionConcreteLi(Dataset[pd.Series]):
    """
    Dataset class for the composition of standard concrete.

    Li (2003) gives a cement content of about 330 kg per m3 of concrete. With
    a concrete density of about 2400 kg/m3, one ton of cement gives about 7.3 t of concrete,
     or 0.1375 t of cement per  t of concrete.
    """

    name = "circularity_demand_reduction_concrete_li"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Advanced concrete technology",
            author=["Z. Li"],
            publication="Elsevier",
            publication_year=2003,
            url="https://doi.org/10.1016/b978-0-7506-5686-3.x5246-x",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            {
                # kg cement per m3 concrete (Li 2003)
                "cement_content": 330.0,
                # kg concrete per m3 concrete (Crista 2024, "The Effectiveness of
                # Styrofoam Mixtures in Lightweight Concrete Walls", Journal of
                # Electrical Systems 20(4s), https://doi.org/10.52783/jes.2805
                "concrete_density": 2400.0,
            },
            name="concrete_composition",
        )

    # -------- methods ------------------------

    def get_concrete_per_cement(self) -> float:
        """
        Get the concrete produced per ton of cement, in t concrete per t cement.
        """
        return float(self.data["concrete_density"] / self.data["cement_content"])

    def get_cement_per_concrete(self) -> float:
        """
        Get the cement needed per ton of concrete, in t cement per t concrete.
        """
        return float(self.data["cement_content"] / self.data["concrete_density"])
