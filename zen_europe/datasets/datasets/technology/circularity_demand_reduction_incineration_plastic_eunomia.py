# demandreductioncircularity: new dataset, plastic waste incineration
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import SourceInformation
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData
from zen_creator.elements import ConversionTechnology
from zen_creator.utils.attribute import Attribute


class CircularityDemandReductionIncinerationPlasticEunomia(Dataset[pd.Series]):
    """
    Dataset class for incineration of plastic waste with electricity recovery.

    Capex, fixed opex and plastic waste input per unit of electric capacity,
    based on Eunomia (costs for municipal waste management in the EU) and Asim
    et al. (2023).
    """

    name = "circularity_demand_reduction_incineration_plastic_eunomia"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Costs for Municipal Waste Management in the EU",
            author=["Eunomia Research & Consulting Ltd."],
            publication=(
                "Final report to Directorate General Environment, "
                "European Commission"
            ),
            publication_year=2002,
            url=(
                "https://ec.europa.eu/environment/pdf/waste/studies/"
                "euwastemanagement_annexes.pdf"
            ),
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            {
                "capex_specific_conversion": 3400000.0,  # Euro/MW_el
                "opex_specific_fixed": 250000.0,  # Euro/MW_el/y
                "plastic_waste": 1100.0,  # t plastic waste per GWh_el
            },
            name="incineration_plastic",
        )

    # -------- methods ------------------------

    def _source(self, what: str) -> SourceInformation:
        return SourceInformation(
            description=(
                f"{what} of plastic waste incineration with electricity recovery, "
                "based on Eunomia (costs for municipal waste management in the EU) "
                "and Asim et al. (2023), Energy Reports 10, 3373-3382."
            ),
            metadata=self.metadata,
        )

    def get_conversion_factor(self, element: ConversionTechnology) -> Attribute:
        """Get the conversion factor: t plastic waste per GWh of electricity."""
        attr = element.conversion_factor
        attr.set_data(
            default_value=[
                {
                    "plastic_waste": {
                        "default_value": float(self.data["plastic_waste"]),
                        "unit": "tproduct/GWh",
                    }
                }
            ],
            source=self._source("Plastic waste input"),
        )
        return attr

    def get_capex_specific_conversion(self, element: ConversionTechnology) -> Attribute:
        """Get the specific capex in Euro/MW_el."""
        attr = element.capex_specific_conversion
        attr.set_data(
            default_value=float(self.data["capex_specific_conversion"]),
            unit="Euro/MW",
            source=self._source("Specific capex"),
        )
        return attr

    def get_opex_specific_fixed(self, element: ConversionTechnology) -> Attribute:
        """Get the specific fixed opex in Euro/MW_el."""
        attr = element.opex_specific_fixed
        attr.set_data(
            default_value=float(self.data["opex_specific_fixed"]),
            unit="Euro/MW",
            source=self._source("Specific fixed opex"),
        )
        return attr
