# demandreductioncircularity: new dataset, costs of chemical plastic recycling
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import SourceInformation
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData
from zen_creator.elements import ConversionTechnology
from zen_creator.utils.attribute import Attribute


class CircularityDemandReductionChemicalRecyclingPlasticGarciaGutierrez(
    Dataset[pd.Series]
):
    """
    Dataset class for the costs of chemical recycling (pyrolysis) of plastic
    waste, per t of olefin.

    (Garcia-Gutierrez et al. 2024; Stallkamp et al. 2024).
    """

    name = "circularity_demand_reduction_chemical_recycling_plastic_garcia_gutierrez"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Environmental and economic assessment of plastic waste recycling "
                "and energy recovery pathways in the EU"
            ),
            author=[
                "P. Garcia-Gutierrez",
                "A. M. Amadei",
                "D. Klenert",
                "S. Nessi",
                "D. Tonini",
                "D. Tosches",
                "F. Ardente",
                "H. G. Saveyn",
            ],
            publication="Resources, Conservation and Recycling, vol. 215, 108099",
            publication_year=2024,
            url="https://doi.org/10.1016/j.resconrec.2024.108099",
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            {
                "capex_specific_conversion": 8600000.0,  # Euro/(t olefin/h)
                "opex_specific_fixed": 1152800.0,  # Euro/(t olefin/h)/y
                "opex_specific_variable": 73.9,  # Euro/t olefin
            },
            name="chemical_recycling_plastic",
        )

    # -------- methods ------------------------

    def _source(self, what: str) -> SourceInformation:
        return SourceInformation(
            description=(
                f"{what} of chemical plastic recycling (pyrolysis), per t of "
                "olefin, based on Garcia-Gutierrez et al. (2024) and Stallkamp "
                "et al. (2024) (2021 Euro)."
            ),
            metadata=self.metadata,
        )

    def get_capex_specific_conversion(self, element: ConversionTechnology) -> Attribute:
        """Get the specific capex in Euro/(t olefin/h)."""
        attr = element.capex_specific_conversion
        attr.set_data(
            default_value=float(self.data["capex_specific_conversion"]),
            unit="Euro/(tproduct/h)",
            source=self._source("Specific capex"),
        )
        return attr

    def get_opex_specific_fixed(self, element: ConversionTechnology) -> Attribute:
        """Get the specific fixed opex in Euro/(t olefin/h)."""
        attr = element.opex_specific_fixed
        attr.set_data(
            default_value=float(self.data["opex_specific_fixed"]),
            unit="Euro/(tproduct/h)",
            source=self._source("Specific fixed opex"),
        )
        return attr

    def get_opex_specific_variable(self, element: ConversionTechnology) -> Attribute:
        """Get the specific variable opex in Euro/t olefin."""
        attr = element.opex_specific_variable
        attr.set_data(
            default_value=float(self.data["opex_specific_variable"]),
            unit="Euro/tproduct",
            source=self._source("Specific variable opex"),
        )
        return attr
