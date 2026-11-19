# demandreductioncircularity: new dataset collection, urban and regional transport
"""Urban and regional passenger transport demand (MSc thesis of U. Bhagole).

- urban transport = buses + trams/metros + 50% of the car passenger-km
- regional transport = trains + the other 50% of the car passenger-km

Annual passenger-km of 2019 from the EU Statistical Pocketbook 2022, hourly
profile from the thesis, modal shares per country from the same passenger-km
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, cast

import pandas as pd

if TYPE_CHECKING:
    from pathlib import Path

    from zen_creator import Dataset

from zen_creator import (
    AssumptionInformation,
    Attribute,
    Carrier,
    ConversionTechnology,
    DatasetCollection,
    SourceInformation,
)
from zen_creator.utils.settings import Settings

from zen_europe.datasets.datasets.carrier.circularity_demand_reduction_passenger_transport_profile_medvid import (  # noqa: E501
    CircularityDemandReductionPassengerTransportProfileMedvid,
)
from zen_europe.datasets.datasets.carrier.circularity_demand_reduction_passenger_transport_rich_mabit import (  # noqa: E501
    CircularityDemandReductionPassengerTransportRichMabit,
)
from zen_europe.datasets.datasets.carrier.standard_load_profiles import (
    StandardLoadProfiles,
)
from zen_europe.datasets.datasets.carrier.statistical_pocketbook_transport import (
    StatisticalPocketbookTransport,
)

# the modal share of a technology may deviate this much (relative) from its
# 2019 share in the reference: min = 0.9 x share, max = 1.1 x share
MODAL_SHARE_BAND = 0.10

# the pocketbook sheet and the transport type of each dummy technology
_DUMMY_MODES = {
    "car_passenger_mileage_to_urban": ("passenger_mileage", "urban"),
    "car_passenger_mileage_to_regional": ("passenger_mileage", "regional"),
    "bus_to_urban": ("bus_mileage", "urban"),
    "tram_metro_to_urban": ("tram_mileage", "urban"),
    "train_passenger_mileage_to_regional": ("train_mileage", "regional"),
}
# the transport type of each final demand carrier
_CARRIER_TYPES = {"urban_transport": "urban", "regional_transport": "regional"}


class CircularityDemandReductionPassengerTransport(DatasetCollection):
    """Urban and regional passenger transport demand and modal shares."""

    name = "circularity_demand_reduction_passenger_transport"

    def __init__(self, settings: Settings, source_path: Path | str):
        self.settings = settings
        super().__init__(source_path=source_path)

    def _get_data(self) -> Dict[str, Dataset[Any]]:
        """Load all available data sources."""

        if self.source_path is None:
            raise ValueError("source_path must be set to load the dataset collection.")

        return {
            "statistical_pocketbook_transport": StatisticalPocketbookTransport(
                self.settings, self.source_path
            ),
            "rich_mabit": CircularityDemandReductionPassengerTransportRichMabit(
                self.source_path
            ),
            "profile_medvid": (
                CircularityDemandReductionPassengerTransportProfileMedvid(
                    self.source_path
                )
            ),
            "standard_load_profiles": StandardLoadProfiles(self.source_path),
        }

    # -------- annual passenger-km ------------------

    def get_mode_contributions(
        self, transport_type: str, nodes: list[str]
    ) -> pd.DataFrame:
        """
        Annual passenger-km of each mode that serves a transport type.

        Modes without a value in the pocketbook (trams in LT and SI, '-') are
        counted as 0. In the thesis input they made the whole urban demand of
        LT and SI missing, i.e. 0.

        Args:
            transport_type: 'urban' or 'regional'.
            nodes: The nodes.

        Returns:
            pd.DataFrame: Million pkm per year, nodes x pocketbook sheets.
        """
        pocketbook = cast(
            StatisticalPocketbookTransport,
            self.data["statistical_pocketbook_transport"],
        )
        rich_mabit = cast(
            CircularityDemandReductionPassengerTransportRichMabit,
            self.data["rich_mabit"],
        )
        contributions = {}
        for mode, mode_type in _DUMMY_MODES.values():
            if mode_type != transport_type:
                continue
            mileage = pocketbook.get_mode_mileage(mode, nodes).fillna(0)
            if mode == "passenger_mileage":
                mileage = mileage * rich_mabit.get_car_share(transport_type)
            contributions[mode] = mileage
        return pd.DataFrame(contributions)

    def get_annual_demand(self, transport_type: str, nodes: list[str]) -> pd.Series:
        """Annual urban or regional passenger transport in million pkm."""
        return self.get_mode_contributions(transport_type, nodes).sum(axis=1)

    # -------- demand ------------------

    def get_demand(self, element: Carrier) -> Attribute:
        """
        Get the hourly demand of urban_transport or regional_transport.

        The annual passenger-km are spread over the hours with the thesis
        profile and shifted by the time zone of each country.
        """
        transport_type = _CARRIER_TYPES[element.name]
        nodes = list(element.model.config.system.set_nodes)
        annual = self.get_annual_demand(transport_type, nodes)
        profile_dataset = cast(
            CircularityDemandReductionPassengerTransportProfileMedvid,
            self.data["profile_medvid"],
        )
        profile = profile_dataset.get_profile(
            element.settings.time.year_time_series, nodes
        )
        demand = profile.mul(annual, axis=1)
        slp_dataset = cast(StandardLoadProfiles, self.data["standard_load_profiles"])
        demand = slp_dataset.shift_by_timezone(demand)
        demand.index.name = "time"
        if transport_type == "urban":
            description = (
                "Urban passenger transport (trips below 100 km): passenger-km of "
                "buses and coaches, trams and metros, and 50% of the passenger "
                "cars (Rich & Mabit 2012), EU Statistical Pocketbook 2022, "
                f"{element.settings.time.year_time_series}. Trams without a value "
                "(LT, SI) count as 0."
            )
        else:
            description = (
                "Regional passenger transport (trips above 100 km): passenger-km "
                "of railways and the other 50% of the passenger cars (Rich & "
                "Mabit 2012), EU Statistical Pocketbook 2022, "
                f"{element.settings.time.year_time_series}."
            )
        description += (
            " The annual passenger-km are spread over the hours with a weekday "
            "and a weekend profile  and shifted by the time zone of each country."
        )
        return element.demand.set_data(
            df=demand,
            unit="megapkm/hour",
            source=SourceInformation(description=description, metadata=self.metadata),
        )

    # -------- modal shares ------------------

    def get_modal_share(self, element: ConversionTechnology) -> pd.Series:
        """
        Share of a dummy technology in the annual urban or regional demand of
        2019, per country.
        """
        mode, transport_type = _DUMMY_MODES[element.name]
        nodes = list(element.model.config.system.set_nodes)
        contributions = self.get_mode_contributions(transport_type, nodes)
        return contributions[mode] / contributions.sum(axis=1)

    def _share_to_df(
        self, element: ConversionTechnology, share: pd.Series, name: str
    ) -> pd.Series:
        """Repeat a share per country over all years, index (node, year)."""
        years = list(element.settings.time.years)
        nodes = list(share.index)
        index = pd.MultiIndex.from_product([nodes, years], names=["node", "year"])
        return pd.Series(
            share.reindex(index.get_level_values("node")).to_numpy(),
            index=index,
            name=name,
        )

    def get_demand_share(
        self, element: ConversionTechnology, attr: Attribute, bound: str
    ) -> Attribute:
        """
        Set the minimum or maximum demand share of a dummy technology to its
        2019 modal share -/+ 10% (relative), equal in all years.

        Args:
            element: The dummy technology.
            attr: demand_share_min or demand_share_max.
            bound: 'min' or 'max'.
        """
        share = self.get_modal_share(element)
        factor = 1 - MODAL_SHARE_BAND if bound == "min" else 1 + MODAL_SHARE_BAND
        df = self._share_to_df(element, (share * factor).clip(upper=1.0), attr.name)
        attr.set_data(
            df=df,
            unit="1",
            source=SourceInformation(
                description=(
                    f"{bound.capitalize()}imum share of {element.name} in the "
                    f"{_DUMMY_MODES[element.name][1]} passenger transport demand: "
                    f"its 2019 modal share x {factor:.1f}, equal in all years "
                    "(EU Statistical Pocketbook 2022 "
                ),
                metadata=self.metadata,
            ),
        )
        attr.add_source(
            AssumptionInformation(
                description=(
                    f"Band of +-{MODAL_SHARE_BAND:.0%} (relative) around the 2019 "
                    "modal share, as in the thesis input. "
                )
            )
        )
        return attr

    def get_modal_share_df(
        self, element: ConversionTechnology, factor: float, name: str
    ) -> pd.Series:
        """The 2019 modal share times a factor, per country and year."""
        return self._share_to_df(element, self.get_modal_share(element) * factor, name)
