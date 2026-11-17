# demandreductioncircularity: new dataset, mechanical plastic recycling (Larrain 2021)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import SourceInformation
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData
from zen_creator.elements import ConversionTechnology
from zen_creator.utils.attribute import Attribute


class CircularityDemandReductionMechanicalRecyclingPlasticLarrain(Dataset[pd.Series]):
    """
    Dataset class for mechanical recycling of post-consumer plastic waste.

    Techno-economic values for a mechanical recycling plant, aggregated over
    polymer types (PP, PE, PS, MPO) with average European consumption shares.
    """

    name = "circularity_demand_reduction_mechanical_recycling_plastic_larrain"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Techno-economic assessment of mechanical recycling of challenging "
                "post-consumer plastic packaging waste"
            ),
            author=[
                "M. Larrain",
                "S. Van Passel",
                "G. Thomassen",
                "B. Van Gorp",
                "T. T. Nhu",
                "S. Huysveld",
                "K. M. Van Geem",
                "S. De Meester",
                "P. Billen",
            ],
            publication="Resources, Conservation and Recycling, vol. 170, 105607",
            publication_year=2021,
            url="https://doi.org/10.1016/j.resconrec.2021.105607",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            {
                "capex_specific_conversion": 3760000.0,  # Euro/(t plastic/h)
                "opex_specific_fixed": 1610000.0,  # Euro/(t plastic/h)/y
                "opex_specific_variable": 47.77,  # Euro/t plastic
                "plastic_waste": 1.25,  # t plastic waste/t plastic
                "electricity": 0.5,  # MWh/t plastic
            },
            name="mechanical_recycling_plastic",
        )

    # -------- methods ------------------------

    def _source(self, what: str) -> SourceInformation:
        return SourceInformation(
            description=(
                f"{what} of mechanical plastic recycling, aggregated over polymer "
                "types with average European consumption shares (2021 Euro)."
            ),
            metadata=self.metadata,
        )

    def get_conversion_factor(self, element: ConversionTechnology) -> Attribute:
        """Get the conversion factor: plastic waste and electricity per t plastic."""
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
            source=self._source("Conversion factor"),
        )
        return attr

    def get_capex_specific_conversion(self, element: ConversionTechnology) -> Attribute:
        """Get the specific capex in Euro/(t plastic/h)."""
        attr = element.capex_specific_conversion
        attr.set_data(
            default_value=float(self.data["capex_specific_conversion"]),
            unit="Euro/(tproduct/h)",
            source=self._source("Specific capex"),
        )
        return attr

    def get_opex_specific_fixed(self, element: ConversionTechnology) -> Attribute:
        """Get the specific fixed opex in Euro/(t plastic/h)."""
        attr = element.opex_specific_fixed
        attr.set_data(
            default_value=float(self.data["opex_specific_fixed"]),
            unit="Euro/(tproduct/h)",
            source=self._source("Specific fixed opex"),
        )
        return attr

    def get_opex_specific_variable(self, element: ConversionTechnology) -> Attribute:
        """Get the specific variable opex in Euro/t plastic."""
        attr = element.opex_specific_variable
        attr.set_data(
            default_value=float(self.data["opex_specific_variable"]),
            unit="Euro/tproduct",
            source=self._source("Specific variable opex"),
        )
        return attr
