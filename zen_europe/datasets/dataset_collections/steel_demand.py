from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, cast

import pandas as pd

from zen_europe.utils.utils import (
    calculate_capacity_addition_from_cumulative,
    format_capacity_existing,
)

if TYPE_CHECKING:
    from pathlib import Path

    from zen_creator import Carrier, Dataset


from zen_creator import Attribute, ConversionTechnology, DatasetCollection
from zen_creator.utils.attribute import SourceInformation

from zen_europe.datasets.datasets.carrier.aidres import Aidres

from zen_europe.datasets.datasets.carrier.circularity_demand_reduction_scrap_steel_jrc import (
    CircularityDemandReductionScrapSteelJRC,
) # demandreductioncircularity
from zen_europe.datasets.datasets.carrier.manual_steel_demand import (
    Eurofer,
    TradeEconomics,
    WorldSteel,
)
from zen_europe.datasets.datasets.carrier.material_economics import MaterialEconomics
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_EAF_cappel import (  # noqa: E501
    CircularityDemandReductionEAFCappel,
) # demandreductioncircularity



class SteelDemand(DatasetCollection):
    """Extracting steel demand data."""

    name = "steel_demand"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> Dict[str, Dataset[Any]]:
        """Load all available data sources."""

        if self.source_path is None:
            raise ValueError("source_path must be set to load the dataset collection.")

        return {
            "aidres": Aidres(self.source_path),
            "eurofer": Eurofer(self.source_path),
            "worldsteel": WorldSteel(self.source_path),
            "trade_economics": TradeEconomics(self.source_path),
            "material_economics": MaterialEconomics(self.source_path),
            # demandreductioncircularity: sources for the scrap steel availability
            "circularity_demand_reduction_scrap_steel_jrc": (
                CircularityDemandReductionScrapSteelJRC(self.source_path)
            ),
            "circularity_demand_reduction_EAF_cappel": (
                CircularityDemandReductionEAFCappel(self.source_path)
            ),
        }

    def _calculate_steel_demand(
        self, element: Carrier
    ) -> tuple[pd.DataFrame, pd.Series]:
        """
        Calculate the steel demand for the given element.
        """
        aidres_dataset = cast(Aidres, self.data["aidres"])
        data = aidres_dataset.get_demand(element)
        eurofer_dataset = cast(Eurofer, self.data["eurofer"])
        worldsteel_dataset = cast(WorldSteel, self.data["worldsteel"])
        trade_economics_dataset = cast(TradeEconomics, self.data["trade_economics"])
        material_economics_dataset = cast(
            MaterialEconomics, self.data["material_economics"]
        )
        missing_countries = pd.Index(element.model.config.system.set_nodes).difference(
            data.index
        )

        for country in missing_countries:
            if country == "CH":
                data.loc[country] = eurofer_dataset.get_manual_steel_demand_eurofer(
                    country
                )
            elif country == "UK":
                data.loc[country] = (
                    worldsteel_dataset.get_manual_steel_demand_worldsteel(country)
                )
            elif country == "NO":
                data.loc[country] = (
                    trade_economics_dataset.get_manual_steel_demand_trade_economics(
                        country
                    )
                )
            else:
                raise ValueError(
                    f"Steel demand data for country {country} is not available in the "
                    "Aidres dataset or any of the manual datasets (Eurofer, "
                    "WorldSteel, TradeEconomics). Please provide the necessary data "
                    "for this country."
                )

        d = data.sort_index() / 8.76

        secondary_steel_share_beginning, secondary_steel_share_end = (
            material_economics_dataset.get_secondary_steel_ratios()
        )
        if element.name == "secondary_steel":
            rat_start = secondary_steel_share_beginning
            rat_end = secondary_steel_share_end / rat_start
        elif element.name in ("steel", "scrap_steel"):
            # demandreductioncircularity: total steel demand (AIDRES, Eurofer,
            # WorldSteel, TradeEconomics), constant over time and not split
            # into primary and secondary steel. The split follows from the
            # scrap steel availability and the demand share of
            # secondary_steel_to_steel (JRC 2021).
            rat_start = 1
            rat_end = 1
        else:
            rat_start = 1 - secondary_steel_share_beginning
            rat_end = (1 - secondary_steel_share_end) / rat_start

        d = d * rat_start
        d.index.name = "node"

        years = element.settings.time.years

        d_yearly_variation = pd.Series(index=years, dtype=float)
        d_yearly_variation.iloc[0] = 1
        d_yearly_variation.iloc[-1] = rat_end
        d_yearly_variation = d_yearly_variation.interpolate(method="index")
        d_yearly_variation.index.name = "year"
        d_yearly_variation.name = "demand_yearly_variation"
        return d, d_yearly_variation

    def get_steel_demand(self, element: Carrier) -> Attribute:
        """
        Get the demand for steel.

        This function retrieves the steel demand data for the specified element.
        """
        d, d_yearly_variation = self._calculate_steel_demand(element)
        source = SourceInformation(
            description=(
                "Steel demand data is derived from multiple sources. The main sourceis "
                "the Aidres dataset. Additional manual data for missing countries is "
                "obtained from the following datasets:Eurofer, WorldSteel, and "
                "TradeEconomics. The secondary steel ratios are derived from the "
                "Material Economics dataset."
            ),
            metadata=self.metadata,
        )
        return element.demand.set_data(
            source=source,
            df=d,
            yearly_variations_df=d_yearly_variation,
            unit="tproduct/h",
        )

    # demandreductioncircularity: scrap steel availability
    def get_scrap_steel_availability(self, element: Carrier) -> Attribute:
        """
        Get the import availability of scrap steel.

        The scrap availability per country and year is the secondary steel share
        of the JRC trajectory times the scrap input of the EAF, applied to the
        total steel demand. This allows exactly the JRC secondary steel share.
        """
        jrc_dataset = cast(
            CircularityDemandReductionScrapSteelJRC,
            self.data["circularity_demand_reduction_scrap_steel_jrc"],
        )
        cappel_dataset = cast(
            CircularityDemandReductionEAFCappel,
            self.data["circularity_demand_reduction_EAF_cappel"],
        )
        years = list(element.settings.time.years)
        share = jrc_dataset.get_secondary_steel_share(years)
        scrap_input = cappel_dataset.get_scrap_steel_input()

        # scrap per t steel demand = secondary steel share * scrap input
        d, _ = self._calculate_steel_demand(element)
        d = d * share.iloc[0] * scrap_input
        d = d.rename(columns={"demand": "availability_import"})

        yearly_variation = share / share.iloc[0]
        yearly_variation.name = "availability_import_yearly_variation"

        source = SourceInformation(
            description=(
                "The scrap steel availability is the secondary steel share of "
                f"the lower-bound JRC trajectory ({share.iloc[0]:.4f} in "
                f"{years[0]}, {share.iloc[-1]:.4f} in {years[-1]}) times the "
                f"EAF scrap input ({scrap_input} t/t, Cappel), applied to the "
                "total steel demand (Aidres, Eurofer, WorldSteel, "
                "TradeEconomics)."
            ),
            metadata=self.metadata,
        )
        return element.availability_import.set_data(
            source=source,
            df=d,
            yearly_variations_df=yearly_variation,
            unit="tproduct/h",
        )
    def get_capacity_existing(self, element: ConversionTechnology) -> Attribute:
        """
        Get the existing capacity for steel production technologies.

        This function retrieves the existing capacity data for the specified element.
        """
        ref_carrier = cast(list[str], element.reference_carrier.default_value)[0]
        if ref_carrier == "secondary_steel":
            assert element.name == "EAF", (
                "The existing capacity for secondary steel production is assumed"
                "to be exclusive the EAF technology."
            )
        elif ref_carrier == "primary_steel":
            assert element.name == "BF_BOF", (
                "The existing capacity for primary steel production is assumed"
                "to be exclusive the BF-BOF technology."
            )
        else:
            raise ValueError(
                f"Unexpected reference carrier '{ref_carrier}' for element "
                f"'{element.name}'."
            )
        steel_demand, _ = self._calculate_steel_demand(
            element.model.carriers[ref_carrier]
        )
        steel_demand = steel_demand.rename(
            {"demand": element.settings.time.reference_year - 1}, axis=1
        )
        capacity_addition = calculate_capacity_addition_from_cumulative(
            steel_demand, element
        )
        capacity_existing = format_capacity_existing(capacity_addition)
        source = SourceInformation(
            description=(
                "It is assumed that all current primary steel demand is based on the "
                "BF-BOF route, and all current secondary steel demand is basedon the "
                "EAF route. Steel demand data is derived from multiple sources. The "
                "main sourceis the Aidres dataset. Additional manual data for missing "
                "countries is obtained from the following datasets:Eurofer, "
                "WorldSteel, and TradeEconomics. The secondary steel ratios are "
                "derived from the Material Economics dataset."
            ),
            metadata=self.metadata,
        )
        return element.capacity_existing.set_data(
            source=source,
            df=capacity_existing,
            unit="tproduct/h",
        )
