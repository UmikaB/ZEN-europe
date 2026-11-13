# demandreductioncircularity: new dataset, concrete fines as kiln feed (CEMBUREAU 2022)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import SourceInformation
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData
from zen_creator.elements import ConversionTechnology
from zen_creator.utils.attribute import Attribute


class CircularityDemandReductionCementFinesCembureau(Dataset[pd.Series]):
    """
    Dataset class for the use of recycled concrete fines as raw material for
    clinker.

    About 1.1 t of concrete fines replace one ton of clinker raw material
    (CEMBUREAU 2022).
    """

    name = "circularity_demand_reduction_cement_fines_cembureau"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Reaching climate neutrality along the cement and concrete value "
                "chain by 2050"
            ),
            author=["European Cement Association (CEMBUREAU)"],
            publication="Tech. Rep., CEMBUREAU 2050 Roadmap",
            publication_year=2022,
            url=(
                "https://cembureau.eu/media/kuxd32gi/"
                "cembureau-2050-roadmap_final-version_web.pdf"
            ),
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            # t concrete fines per t clinker input material
            {"concrete_fine": 1.10},
            name="conversion_factor",
        )

    # -------- methods ------------------------

    def get_conversion_factor_cement_fines_for_clinker(
        self, element: ConversionTechnology
    ) -> Attribute:
        """
        Get the conversion factor of cement_fines_for_clinker, in t concrete fines
        per t clinker input material.
        """
        attr = element.conversion_factor
        value = float(self.data["concrete_fine"])
        attr.set_data(
            default_value=[
                {"concrete_fine": {"default_value": value, "unit": "tproduct/tproduct"}}
            ],
            source=SourceInformation(
                description=(
                    f"About {value} t of recycled concrete fines replace one ton of "
                    "raw material for clinker production."
                ),
                metadata=self.metadata,
            ),
        )
        return attr
