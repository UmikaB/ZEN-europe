# demandreductioncircularity: new dataset, capex of cement recycling (CORDIS 2014)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import SourceInformation
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData
from zen_creator.elements import ConversionTechnology
from zen_creator.utils.attribute import Attribute


class CircularityDemandReductionCementRecyclingCORDIS(Dataset[pd.Series]):
    """
    Dataset class for the capital cost of recovering unhydrated cement from
    concrete waste.

    Based on the EU project C2CA, "Advanced Technologies for the Production of
    Cement and Clean Aggregates from Construction and Demolition Waste"
    (CORDIS project 265189).
    """

    name = "circularity_demand_reduction_cement_recycling_cordis"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Advanced Technologies for the Production of Cement and Clean "
                "Aggregates from Construction and Demolition Waste"
            ),
            author=["CORDIS, European Commission"],
            publication="CORDIS project 265189, reporting",
            publication_year=2014,
            url="https://cordis.europa.eu/project/id/265189/reporting/fr",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            # Euro per (t cement/h)
            {"capex_specific_conversion": 400000.0},
            name="capex",
        )

    # -------- methods ------------------------

    def get_capex_specific_cement_recycling(
        self, element: ConversionTechnology
    ) -> Attribute:
        """
        Get the specific capex of cement_recycling, in Euro per (t cement/h).

        The value is used as in the thesis, without inflation correction.
        """
        attr = element.capex_specific_conversion
        value = float(self.data["capex_specific_conversion"])
        attr.set_data(
            default_value=value,
            unit="Euro/(tproduct/h)",
            source=SourceInformation(
                description=(
                    "Specific capex of recovering unhydrated cement particles from "
                    "concrete waste, based on the C2CA project (CORDIS 265189). "
                ),
                metadata=self.metadata,
            ),
        )
        return attr
