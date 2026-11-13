from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, cast

import pandas as pd

from zen_europe.datasets.datasets.carrier.material_economics import MaterialEconomics
from zen_europe.utils.constants import Constants
from zen_europe.utils.utils import (
    calculate_capacity_addition_from_cumulative,
    format_capacity_existing,
)

if TYPE_CHECKING:
    from pathlib import Path

    from zen_creator import Carrier, Dataset


from zen_creator import (
    Attribute,
    ConversionTechnology,
    DatasetCollection,
    RetrofittingTechnology,
)
from zen_creator.utils.attribute import SourceInformation

from zen_europe.datasets.datasets.carrier.aidres import Aidres
from zen_europe.datasets.datasets.carrier.british_geological_survey import (
    BritishGeologicalSurvey,
)
from zen_europe.datasets.datasets.carrier.circularity_demand_reduction_concrete_li import (
    CircularityDemandReductionConcreteLi,  # demandreductioncircularity
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_cement_recycling_moreno_juez import (  # noqa: E501
    CircularityDemandReductionCementRecyclingMorenoJuez,  # demandreductioncircularity
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_cement_recycling_van_ekenstein import (  # noqa: E501
    CircularityDemandReductionCementRecyclingVanEkenstein,  # demandreductioncircularity
)
from zen_europe.datasets.datasets.technology.circularity_demand_reduction_cement_to_concrete_mpa import (  # noqa: E501
    CircularityDemandReductionCementToConcreteMPA,  # demandreductioncircularity
)
from zen_europe.datasets.datasets.technology.ecra_technology_papers import (
    ECRATechnologyPapers,
)


class ClinkerData(DatasetCollection):
    """Extracting clinker data data."""

    name = "clinker_data"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> Dict[str, Dataset[Any]]:
        """Load all available data sources."""

        if self.source_path is None:
            raise ValueError("source_path must be set to load the dataset collection.")

        return {
            "aidres": Aidres(self.source_path),
            "british_geological_survey": BritishGeologicalSurvey(self.source_path),
            "material_economics": MaterialEconomics(self.source_path),
            "ecra_technology_papers": ECRATechnologyPapers(self.source_path),
            # demandreductioncircularity: datasets of the concrete chain
            "circularity_demand_reduction_concrete_li": (
                CircularityDemandReductionConcreteLi(self.source_path)
            ),
            "circularity_demand_reduction_cement_to_concrete_mpa": (
                CircularityDemandReductionCementToConcreteMPA(self.source_path)
            ),
            "circularity_demand_reduction_cement_recycling_van_ekenstein": (
                CircularityDemandReductionCementRecyclingVanEkenstein(self.source_path)
            ),
            "circularity_demand_reduction_cement_recycling_moreno_juez": (
                CircularityDemandReductionCementRecyclingMorenoJuez(self.source_path)
            ),
        }

    def _calculate_clinker_demand(self, element: Carrier) -> pd.DataFrame:
        """
        Calculate the clinker demand for the given element.

        This function retrieves the clinker demand data for the specified element.
        It first attempts to get the demand from the Aidres dataset. If the demand
        data is not available in Aidres, it falls back to using data from the
        British Geological Survey (BGS) dataset.

        Args:
            element (Carrier): The carrier for which to calculate clinker demand.

        Returns:
            pd.DataFrame: The clinker demand data.
        """
        aidres_dataset = cast(Aidres, self.data["aidres"])
        data = aidres_dataset.get_demand(element)
        bgs_dataset = cast(
            BritishGeologicalSurvey, self.data["british_geological_survey"]
        )

        missing_countries = pd.Index(element.model.config.system.set_nodes).difference(
            data.index
        )

        for country in missing_countries:
            data.loc[country] = bgs_dataset.get_manual_cement_demand(country)

        data = data.sort_index() / 8.76 * aidres_dataset.get_CEM2_clinker_ratio()

        data.index.name = "node"
        return data

    def get_clinker_demand(self, element: Carrier) -> Attribute:
        """
        Get the demand for clinker.

        This function retrieves the clinker demand data for the specified element.
        """
        data = self._calculate_clinker_demand(element)

        source = SourceInformation(
            description=(
                "Clinker demand data is derived from the Aidres dataset, which "
                "provides demand data for various industrial sectors. For countries "
                "not covered in the Aidres dataset,  cement demand data from the "
                "British Geological Survey is used."
            ),
            metadata=self.metadata,
        )
        return element.demand.set_data(
            source=source,
            df=data,
            unit="tproduct/h",
        )

    def get_conversion_factor_cement_kiln(
        self, element: ConversionTechnology
    ) -> Attribute:
        """
        Get the conversion factor for cement.

        This function retrieves the cement conversion factor data for the specified
        element.

        The reference cement fuel is hard coal, which can be substituted by other fuels
        in the model.
        """
        attr = element.conversion_factor
        aidres_dataset = cast(Aidres, self.data["aidres"])
        me_dataset = cast(MaterialEconomics, self.data["material_economics"])
        cement_to_clinker = aidres_dataset.get_CEM2_clinker_ratio()
        fuel_consumption_kiln = me_dataset.get_fuel_consumption_cement_kiln()
        cf = [
            {
                "electricity": {
                    "default_value": (
                        0.29 / (Constants.GJ_PER_MWH * 1000) / cement_to_clinker
                    ),
                    "unit": "GWh/tproduct",
                }
            },
            {
                "fuel_for_cement": {
                    "default_value": (
                        fuel_consumption_kiln / (Constants.GJ_PER_MWH * 1000)
                    ),
                    "unit": "GWh/tproduct",
                }
            },
            # demandreductioncircularity: raw material input of the kiln
            {
                "clinker_input_material": {
                    "default_value": 1.0,
                    "unit": "tproduct/tproduct",
                }
            },
        ]
        attr.set_data(
            default_value=cf,
            source=SourceInformation(
                description=(
                    "The conversion factor of cement kilns is "
                    "derived from a fuel consumption of 3.7 GJ per ton of "
                    "clinker  (Material Economics) and an "
                    "electricity consumption of 0.29 GJ per ton of cement (AIDRES), "
                    "rescaled to a clinker basis via the AIDRES "
                    "clinker-to-cement ratio of 0.70."
                    " The reference cement fuel is hard coal, which can be substituted "
                    "by other fuels in the model ('<x>_to_cement_fuel')."
                ),
                metadata=self.metadata,
            ),
        )
        return attr

    def get_retrofit_flow_coupling_factor(
        self, element: RetrofittingTechnology
    ) -> Attribute:
        """
        Get the retrofit flow coupling factor for cement fuel.

        The factor limits the fuel a cement fuel technology supplies to the share of
        the kiln fuel demand that this fuel can cover at most. It is therefore the
        product of the substitution potential of the fuel and the fuel consumption of
        the cement kiln, both per ton of clinker.
        """
        attr = element.retrofit_flow_coupling_factor
        me_dataset = cast(MaterialEconomics, self.data["material_economics"])
        ecra_dataset = cast(ECRATechnologyPapers, self.data["ecra_technology_papers"])
        fuel_consumption_kiln = me_dataset.get_fuel_consumption_cement_kiln()
        substitution_potential = ecra_dataset.get_substitution_potential(element.name)
        attr.set_data(
            default_value=(
                substitution_potential
                * fuel_consumption_kiln
                / (Constants.GJ_PER_MWH * 1000)
            ),
            unit="GWh/tproduct",
            source=SourceInformation(
                description=(
                    "The retrofit flow coupling factor of cement fuel technologies is "
                    "the product of the substitution potential of the fuel "
                    f"({substitution_potential:.0%} of the kiln fuel demand, ECRA "
                    "(2022), Technology Papers 2022) and the fuel consumption of the "
                    "cement kiln of 3.7 GJ per ton of clinker (Material Economics "
                    "(2019), 'Industrial Transformation 2050')."
                ),
                metadata=self.metadata,
            ),
        )
        return attr

    def get_capacity_existing_cement_fuel(
        self, element: ConversionTechnology
    ) -> Attribute:
        """
        Get the existing capacity for cement fuel.

        This function retrieves the existing capacity data for cement fuel technologies.
        """
        attr = element.capacity_existing
        aidres_dataset = cast(Aidres, self.data["aidres"])
        me_dataset = cast(MaterialEconomics, self.data["material_economics"])
        share = aidres_dataset.get_share_capacity_existing_cement_fuel()
        assert (
            element.name in share
        ), f"Existing capacity share for {element.name} not found."
        clinker_element = element.model.carriers["clinker"]
        clinker_demand = self._calculate_clinker_demand(clinker_element)
        clinker2fuel = me_dataset.get_fuel_consumption_cement_kiln() / 3600  # GWh/t
        clinker_demand = clinker_demand.rename(
            {"demand": element.settings.time.reference_year - 1}, axis=1
        )
        clinker_demand *= clinker2fuel * share[element.name]
        capacity_addition = calculate_capacity_addition_from_cumulative(
            clinker_demand, element
        )
        capacity_existing = format_capacity_existing(capacity_addition)
        attr.set_data(
            df=capacity_existing,
            unit="GW",
            source=SourceInformation(
                description=(
                    "The existing capacity for cement fuel technologies is mainly "
                    "derived from the Aidres dataset, which provides "
                    "data on existing capacities for various industrial sectors."
                ),
                metadata=self.metadata,
            ),
        )
        return attr
 # demandreductioncircularity: new method, final demand of concrete use
    def get_concrete_demand(self, element: Carrier) -> Attribute:
        """
        Get the demand for concrete use.

        The cement demand (Aidres, completed with the British Geological Survey)
        is converted to concrete with about 7.27 t of concrete per t of cement
        (2400 kg/m3 concrete density, 330 kg/m3 cement content).
        """
        aidres_dataset = cast(Aidres, self.data["aidres"])
        li_dataset = cast(
            CircularityDemandReductionConcreteLi,
            self.data["circularity_demand_reduction_concrete_li"],
        )
        # _calculate_clinker_demand gives clinker, so divide by the clinker ratio
        cement_demand = (
            self._calculate_clinker_demand(element)
            / aidres_dataset.get_CEM2_clinker_ratio()
        )
        concrete_per_cement = li_dataset.get_concrete_per_cement()
        data = cement_demand * concrete_per_cement
        source = SourceInformation(
            description=(
                "Concrete use demand is derived from the cement demand of the Aidres "
                "dataset, completed with cement demand data from the British "
                "Geological Survey for countries not covered in Aidres. All cement "
                f"is assumed to be used in concrete, with {concrete_per_cement:.2f} "
                "t of concrete per t of cement (concrete density of 2400 kg/m3, "
                "Crista 2024; cement content of 330 kg/m3, Li 2003)."
            ),
            metadata=self.metadata,
        )
        return element.demand.set_data(
            source=source,
            df=data,
            unit="tproduct/h",
        )

    # demandreductioncircularity: new method, cement_to_concrete
    def get_conversion_factor_cement_to_concrete(
        self, element: ConversionTechnology
    ) -> Attribute:
        """
        Get the conversion factor of cement_to_concrete: the cement content of
        concrete (Li 2003, Crista 2024) and the electricity use of ready-mixed
        concrete production (MPA UK 2024).
        """
        attr = element.conversion_factor
        li_dataset = cast(
            CircularityDemandReductionConcreteLi,
            self.data["circularity_demand_reduction_concrete_li"],
        )
        mpa_dataset = cast(
            CircularityDemandReductionCementToConcreteMPA,
            self.data["circularity_demand_reduction_cement_to_concrete_mpa"],
        )
        cement = li_dataset.get_cement_per_concrete()
        electricity = mpa_dataset.get_electricity_per_concrete()
        attr.set_data(
            default_value=[
                {"cement": {"default_value": cement, "unit": "tproduct/tproduct"}},
                {"electricity": {"default_value": electricity, "unit": "GWh/tproduct"}},
            ],
            source=SourceInformation(
                description=(
                    f"Cement to concrete needs {cement:.4f} t of cement per t of "
                    "concrete (cement content of 330 kg/m3, Li 2003; concrete density "
                    f"of 2400 kg/m3, Crista 2024) and {electricity * 1000:.5f} MWh of "
                    "electricity per t of concrete (MPA UK 2024, sector EPD for "
                    "ready-mixed concrete)."
                ),
                metadata=self.metadata,
            ),
        )
        return attr

    # demandreductioncircularity: new method, cement_recycling
    def get_conversion_factor_cement_recycling(
        self, element: ConversionTechnology
    ) -> Attribute:
        """
        Get the conversion factor of cement_recycling (recovery of unhydrated
        cement from concrete waste): the concrete waste input (Van Ekenstein et
        al. 2024) and the electricity use (Moreno-Juez et al. 2020).
        """
        attr = element.conversion_factor
        van_ekenstein_dataset = cast(
            CircularityDemandReductionCementRecyclingVanEkenstein,
            self.data["circularity_demand_reduction_cement_recycling_van_ekenstein"],
        )
        moreno_juez_dataset = cast(
            CircularityDemandReductionCementRecyclingMorenoJuez,
            self.data["circularity_demand_reduction_cement_recycling_moreno_juez"],
        )
        waste = van_ekenstein_dataset.get_concrete_waste_per_cement()
        electricity = moreno_juez_dataset.get_electricity_per_cement()
        attr.set_data(
            default_value=[
                {
                    "concrete_waste": {
                        "default_value": waste,
                        "unit": "tproduct/tproduct",
                    }
                },
                {"electricity": {"default_value": electricity, "unit": "GWh/tproduct"}},
            ],
            source=SourceInformation(
                description=(
                    f"Recovering one ton of unhydrated cement needs {waste} t of "
                    "concrete waste (Van Ekenstein et al. 2024) and "
                    f"{electricity * 1000:.3f} MWh of electricity (Moreno-Juez et al. "
                    "2020, heating-air classification)."
                ),
                metadata=self.metadata,
            ),
        )
        return attr
