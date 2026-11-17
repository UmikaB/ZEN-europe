# demandreductioncircularity: new dataset, pyrolysis of plastic waste (Stallkamp 2024)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import SourceInformation
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData
from zen_creator.elements import ConversionTechnology
from zen_creator.utils.attribute import Attribute


class CircularityDemandReductionChemicalRecyclingPlasticStallkamp(Dataset[pd.Series]):
    """
    Dataset class for the material and electricity input of chemical recycling
    (pyrolysis) of plastic waste.

    About 5.05 t of plastic waste and 0.3 MWh of electricity per t of olefin.

    """

    name = "circularity_demand_reduction_chemical_recycling_plastic_stallkamp"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Pyrolysis of mixed engineering plastics: Economic challenges for "
                "automotive plastic waste"
            ),
            author=[
                "C. Stallkamp",
                "M. Hennig",
                "R. Volk",
                "D. Stapf",
                "F. Schultmann",
            ],
            publication="Waste Management, vol. 176, pp. 105-116",
            publication_year=2024,
            url="https://doi.org/10.1016/j.wasman.2024.01.035",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            {
                "plastic_waste": 5.05,  # t plastic waste/t olefin
                "electricity": 0.3,  # MWh/t olefin
            },
            name="chemical_recycling_plastic",
        )

    # -------- methods ------------------------

    def get_conversion_factor(self, element: ConversionTechnology) -> Attribute:
        """Get the conversion factor: plastic waste and electricity per t olefin."""
        attr = element.conversion_factor
        attr.set_data(
            default_value=[
                {
                    "plastic_waste": {
                        "default_value": float(self.data["plastic_waste"]),
                        "unit": "tproduct/tproduct",
                    }
                },
                {
                    "electricity": {
                        "default_value": float(self.data["electricity"]) / 1000,
                        "unit": "GWh/tproduct",
                    }
                },
            ],
            source=SourceInformation(
                description=(
                    "Chemical recycling (pyrolysis) needs about 5.05 t of plastic "
                    "waste and 0.3 MWh of electricity per t of olefin."
                ),
                metadata=self.metadata,
            ),
        )
        return attr
