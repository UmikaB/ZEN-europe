# demandreductioncircularity: new dataset, scrap steel input of the EAF (Cappel 2021)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import SourceInformation
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData
from zen_creator.utils.attribute import Attribute


class CircularityDemandReductionEAFCappel(Dataset[pd.Series]):
    """
    Dataset class for the scrap steel input of the electric arc furnace (EAF).

    Cappel (2021) gives the metallic yield of the EAF. About 1.1 t of scrap is
    needed per t of liquid steel, accounting for processing losses.
    """


class CircularityDemandReductionEAFCappel(Dataset[pd.Series]):
    """
    Dataset class for the scrap steel input of the electric arc furnace (EAF).

    Cappel (2021) gives the metallic yield of the EAF. About 1.1 t of scrap is
    needed per t of liquid steel, accounting for processing losses. Used in the
    MSc thesis of U. Bhagole, Section 3.2.2, reference [78].
    """

    name = "circularity_demand_reduction_EAF_cappel"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="EAF Efficiency",
            author=["J. Cappel", "Cappel Stahl Consulting GmbH"],
            publication="Tech. Rep., AIST MENA conference presentation",
            publication_year=2021,
            url=(
                "https://www.aist.org/AIST/aist/AIST/Conferences_Exhibitions/MENA/"
                "Presentations/AIST_MENA_EAF-Efficiency_Cappel.pdf"
            ),
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            # t scrap steel per t secondary steel
            {"scrap_steel": 1.1},
            name="conversion_factor",
        )


    def get_scrap_steel_input(self) -> float:
        """
        Get the scrap steel input of the EAF in t scrap per t secondary steel.
        """
        return float(self.data["scrap_steel"])

    def add_scrap_steel_to_conversion_factor(self, attr: Attribute) -> Attribute:
        """
        Add the scrap steel input to an existing conversion factor of the EAF.

        Args:
            attr: The conversion factor of the EAF with the energy inputs.

        Returns:
            Attribute: The conversion factor including scrap steel.
        """
        value = self.get_scrap_steel_input()
        cf = list(attr.default_value) + [
            {"scrap_steel": {"default_value": value, "unit": "tproduct/tproduct"}}
        ]
        attr.set_data(
            default_value=cf,
            source=SourceInformation(
                description=(
                    f"The EAF needs {value} t scrap steel per t secondary steel, "
                    "accounting for processing losses."
                ),
                metadata=self.metadata,
            ),
        )
        return attr
