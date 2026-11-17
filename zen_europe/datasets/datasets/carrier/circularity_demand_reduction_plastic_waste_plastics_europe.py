# demandreductioncircularity: new dataset, plastic waste recycling shares today
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import SourceInformation
from zen_creator.datasets.datasets.dataset import Dataset
from zen_creator.datasets.datasets.metadata import MetaData
from zen_creator.elements import ConversionTechnology
from zen_creator.utils.attribute import Attribute


class CircularityDemandReductionPlasticWastePlasticsEurope(Dataset[pd.Series]):
    """
    Dataset class for today's recycling shares of post-consumer plastic waste.

    In 2022, EU27+3 post-consumer plastic waste treatment amounted to 26.8%
    recycling (8.7 Mt of 32.3 Mt), almost all mechanical. Chemical recycling
    played a negligible role. The reference scenario keeps these shares
    constant: mechanical recycling exactly 26.8%, chemical recycling 0%. The
    ratio of waste to plastics demand is the basis for the 0.67 t of waste per t
    of plastic use.
    """

    name = "circularity_demand_reduction_plastic_waste_plastics_europe"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Plastics Europe report",
            author=["Plastics Europe"],
            publication="Plastics Europe, Tech. Rep.",
            publication_year=2023,
            url=(
                "https://plasticseurope.org/wp-content/uploads/2023/10/"
                "PlasticsEurope_Report_24.10.pdf"
            ),
        )

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series(
            {
                # share of post-consumer plastic waste, mechanically recycled
                "mechanical_recycling_plastic": 0.268,
                # chemical recycling, negligible, set to 0 in the reference
                "chemical_recycling_plastic": 0.0,
                # Mt post-consumer plastic waste collected, EU27+3 2022
                "waste_collected": 32.3,
                # Mt converted plastics demand, EU27+3 2022 (7.3 Mt = 13.5%)
                "converted_demand": 54.0,
                # Mt circular plastics in converted demand
                "circular_plastics": 7.3,
                # t plastic waste per t plastic use, as used in the thesis
                "waste_per_plastic_use": 0.67,
            },
            name="recycling_share",
        )

    # -------- methods ------------------------

    def get_recycling_share(self, technology: str) -> float:
        """
        Get the share of plastic waste treated by a recycling technology today.
        """
        return float(self.data[technology])

    def get_waste_per_plastic_use(self) -> float:
        """
        Get the plastic waste generated per ton of plastic use, in t/t.

        Post-consumer waste (32.3 Mt) relative to converted plastics demand gives
        0.60 (total demand, 54 Mt) to 0.69 (virgin demand, 54 - 7.3 Mt). The
        thesis uses 0.67, within this range.
        """
        return float(self.data["waste_per_plastic_use"])

    def get_conversion_factor_overproduction_use_plastic(
        self, element: ConversionTechnology
    ) -> Attribute:
        """
        Get the conversion factor of overproduction_use_plastic: one ton of
        plastic per ton of plastic use, and the plastic waste generated.
        """
        waste = self.get_waste_per_plastic_use()
        low = self.data["waste_collected"] / self.data["converted_demand"]
        high = self.data["waste_collected"] / (
            self.data["converted_demand"] - self.data["circular_plastics"]
        )
        attr = element.conversion_factor
        attr.set_data(
            default_value=[
                {"plastic": {"default_value": 1.0, "unit": "tproduct/tproduct"}},
                {
                    "plastic_waste": {
                        "default_value": waste,
                        "unit": "tproduct/tproduct",
                    }
                },
            ],
            source=SourceInformation(
                description=(
                    "Dummy technology that splits plastic into plastic use and "
                    "plastic waste. One ton of plastic gives one ton of plastic use "
                    f"(assumption) and {waste} t of plastic waste. Basis: EU27+3 2022 "
                    "post-consumer plastic waste (32.3 Mt) relative to converted "
                    f"plastics demand (about 54 Mt, of which 7.3 Mt circular) gives "
                    f"{low:.2f} (total demand) to {high:.2f} (virgin demand); the MSc "
                    "thesis of U. Bhagole uses 0.67, within this range."
                ),
                metadata=self.metadata,
            ),
        )
        return attr
