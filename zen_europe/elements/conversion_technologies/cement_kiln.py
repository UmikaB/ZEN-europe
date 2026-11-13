from __future__ import annotations

from typing import TYPE_CHECKING

from zen_europe.datasets.dataset_collections.clinker_data import ClinkerData
from zen_europe.datasets.datasets.carrier.material_economics import MaterialEconomics
from zen_europe.datasets.datasets.technology.cement_production_gardarsdottir import (
    CementProductionGardarsdottir,
)
from zen_europe.utils.circularity_demand_reduction_scenarios import (
    CEMENT_KILN_ENERGY_FACTOR,  # demandreductioncircularity
    EFFICIENCY_IMPROVEMENTS,  # demandreductioncircularity
    scale_conversion_factor,  # demandreductioncircularity
)

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import Attribute, ConversionTechnology, Scenario


class CementKiln(ConversionTechnology):
    """Class containing all data and assumptions for cement kilns (clinker
    production)."""

    name: str = "cement_kiln"

    def __init__(self, model: Model, power_unit: str = "tproduct/h"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Sets the reference carrier of cement kilns to clinker.
        """
        return Attribute(
            name="reference_carrier", default_value=["clinker"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Sets the input carrier of cement kilns to fuel for cement and
        electricity.
        """
        return Attribute(
            name="input_carrier",
            # demandreductioncircularity: clinker_input_material added as input
            default_value=["fuel_for_cement", "electricity", "clinker_input_material" ],
            element=self,
        )

    def _set_output_carrier(self) -> Attribute:
        """
        Set the output carrier of cement kilns to clinker.
        """
        return Attribute(name="output_carrier", default_value=["clinker"], element=self)

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Sets the lifetime of cement kilns.

        """
        cement_dataset = CementProductionGardarsdottir(source_path=self.source_path)
        return cement_dataset.get_lifetime(self)

    def _set_construction_time(self) -> Attribute:
        """
        Sets the construction time of cement kilns.

        """
        if self.settings.investment.use_construction_times:
            cement_dataset = CementProductionGardarsdottir(source_path=self.source_path)
            return cement_dataset.get_construction_time(self)
        else:
            return self.construction_time

    def _set_conversion_factor(self) -> Attribute:
        """
        Return the conversion factor of cement kilns.

        """
        clinker_demand_dataset = ClinkerData(source_path=self.source_path)
        attr = clinker_demand_dataset.get_conversion_factor_cement_kiln(self)
        # demandreductioncircularity: efficiency improvements, kiln energy -10%
        attr.add_scenarios(
            Scenario(
                EFFICIENCY_IMPROVEMENTS,
                default_value=scale_conversion_factor(
                    attr.default_value,
                    {
                        "fuel_for_cement": CEMENT_KILN_ENERGY_FACTOR,
                        "electricity": CEMENT_KILN_ENERGY_FACTOR,
                    },
                ),
            )
        )
        return attr

    def _set_carbon_intensity_technology(self) -> Attribute:
        """
        Sets the carbon intensity of cement kilns.

        Returns:
            Attribute: An Attribute object containing the carbon intensity data.
        """
        material_economics_dataset = MaterialEconomics(source_path=self.source_path)
        return material_economics_dataset.get_clinker_carbon_intensity(self)

    def _set_capex_specific_conversion(self) -> Attribute:
        """
        Sets the specific conversion capital expenditure (capex) for cement
        kilns.

        Returns:
            Attribute: An Attribute object containing the specific conversion capex
                data.
        """
        cement_dataset = CementProductionGardarsdottir(source_path=self.source_path)
        return cement_dataset.get_capex_specific(self)

    def _set_opex_specific_fixed(self) -> Attribute:
        """
        Sets the specific fixed operational expenditure (opex) for cement
        kilns.

        Returns:
            Attribute: An Attribute object containing the specific fixed opex data.
        """
        cement_dataset = CementProductionGardarsdottir(source_path=self.source_path)
        return cement_dataset.get_opex_specific_fixed(self)

    def _set_opex_specific_variable(self) -> Attribute:
        """
        Sets the specific variable operational expenditure (opex) for cement
        kilns.

        Returns:
            Attribute: An Attribute object containing the specific variable opex data.
        """
        cement_dataset = CementProductionGardarsdottir(source_path=self.source_path)
        return cement_dataset.get_opex_specific_variable(self)
