# demandreductioncircularity: new dataset, concrete waste generation (EEA 2020)
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import SourceInformation
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData
from zen_creator.elements import ConversionTechnology
from zen_creator.utils.attribute import Attribute


class CircularityDemandReductionConcreteWasteEEA(Dataset[pd.Series]):
    """
    Dataset class for the concrete waste generated per ton of concrete used.

    The EU generates about 531 Mt of construction and demolition (C&D) waste per
    year (EEA 2020; Eurostat 2024), of which 50-70% is concrete and masonry
    (CEMBUREAU 2022, ref. [95]). The midpoint of 60%  gives about 320 Mt of concrete
    waste per year. EU cement consumption was 167  Mt in 2021 (Harder 2023), or about
    1200 Mt of concrete. Waste generation is therefore about 25% of concrete consumption.
    """

    name = "circularity_demand_reduction_concrete_waste_eea"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Construction and demolition waste: challenges and opportunities in "
                "a circular economy"
            ),
            author=["European Environment Agency (EEA)"],
            publication="European Environment Agency, Copenhagen",
            publication_year=2020,
            url=(
                "https://www.eea.europa.eu/en/analysis/publications/"
                "construction-and-demolition-waste-challenges"
            ),
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            {
                # Mt C&D waste per year in the EU (EEA 2020,  Eurostat 2024)
                "cd_waste": 531.0,
                # share of concrete and masonry in C&D waste, midpoint of 50-70%
                # (CEMBUREAU 2022)
                "concrete_share_cd_waste": 0.60,
                # Mt cement consumption in the EU in 2021 (Harder 2023)
                "cement_consumption": 167.0,
                # t concrete waste per t concrete used, as adopted in the thesis
                "concrete_waste_per_concrete_use": 0.25,
            },
            name="concrete_waste",
        )

    # -------- methods ------------------------

    def get_concrete_waste_per_concrete_use(self) -> float:
        """
        Get the concrete waste per ton of concrete used, in t/t.
        """
        return float(self.data["concrete_waste_per_concrete_use"])

    def get_conversion_factor_concrete_demolishment(
        self, element: ConversionTechnology
    ) -> Attribute:
        """
        Get the conversion factor of concrete_demolishment_overproduction.

        Per ton of concrete use (reference carrier), one ton of concrete is
        needed and 0.25 t of concrete waste is generated.
        """
        attr = element.conversion_factor
        waste = self.get_concrete_waste_per_concrete_use()
        attr.set_data(
            default_value=[
                {"concrete": {"default_value": 1.0, "unit": "tproduct/tproduct"}},
                {
                    "concrete_waste": {
                        "default_value": waste,
                        "unit": "tproduct/tproduct",
                    }
                },
            ],
            source=SourceInformation(
                description=(
                    "Dummy technology that splits concrete into concrete use and "
                    "concrete waste. One ton of concrete gives one ton of concrete "
                    f"use (assumption) and {waste} t of concrete waste: about 531 Mt "
                    "of C&D waste per year in the EU (EEA 2020; Eurostat 2024), "
                    "60% of it concrete and masonry (CEMBUREAU 2022), compared with "
                    "about 1200 Mt of concrete from 167 Mt of cement (Harder 2023)."
                ),
                metadata=self.metadata,
            ),
        )
        return attr
