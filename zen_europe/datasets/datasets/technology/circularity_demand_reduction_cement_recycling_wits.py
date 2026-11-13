# demandreductioncircularity: new dataset, variable opex of cement recycling
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import SourceInformation
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData
from zen_creator.elements import ConversionTechnology
from zen_creator.utils.attribute import Attribute


class CircularityDemandReductionCementRecyclingWITS(Dataset[pd.Series]):
    """
    Dataset class for the variable operating cost of recovering unhydrated
    cement from concrete waste.

    """

    name = "circularity_demand_reduction_cement_recycling_wits"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="European Union imports of gypsum, anhydrite",
            author=["World Integrated Trade Solution (WITS), World Bank"],
            publication="WITS trade statistics",
            publication_year=2023,
            url="https://wits.worldbank.org/",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            # Euro per t cement
            {"opex_specific_variable": 2.5},
            name="opex",
        )

    # -------- methods ------------------------

    def get_opex_specific_variable_cement_recycling(
        self, element: ConversionTechnology
    ) -> Attribute:
        """
        Get the specific variable opex of cement_recycling, in Euro per t cement.
        """
        attr = element.opex_specific_variable
        value = float(self.data["opex_specific_variable"])
        attr.set_data(
            default_value=value,
            unit="Euro/tproduct",
            source=SourceInformation(
                description=(
                    f"Variable opex of {value} Euro per t recovered cement, derived "
                    "from EU trade data for gypsum and anhydrite (WITS 2023), the "
                    "EU gypsum market report (IndexBox 2024) and the cement raw "
                    "materials profile (British Geological Survey 2005)."
                ),
                metadata=self.metadata,
            ),
        )
        return attr
