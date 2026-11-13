from zen_creator import Sector

from zen_europe.elements.carriers.cement import Cement  # demandreductioncircularity
from zen_europe.elements.carriers.clinker import Clinker
from zen_europe.elements.carriers.clinker_input_material import (
    ClinkerInputMaterial,  # demandreductioncircularity
)
from zen_europe.elements.carriers.concrete import Concrete  # demandreductioncircularity
from zen_europe.elements.carriers.concrete_fine import (
    ConcreteFine,  # demandreductioncircularity
)
from zen_europe.elements.carriers.concrete_use import (
    ConcreteUse,  # demandreductioncircularity
)
from zen_europe.elements.carriers.concrete_waste import (
    ConcreteWaste,  # demandreductioncircularity
)
from zen_europe.elements.carriers.fuel_for_cement import FuelForCement
from zen_europe.elements.carriers.raw_material_clinker import (
    RawMaterialClinker,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.cement_fines_for_clinker import (
    CementFinesForClinker,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.cement_kiln import CementKiln
from zen_europe.elements.conversion_technologies.cement_recycling import (
    CementRecycling,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.cement_to_concrete import (
    CementToConcrete,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.clinker_to_cement import (
    ClinkerToCement,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.concrete_demolishment_overproduction import (  # noqa: E501
    ConcreteDemolishmentOverproduction,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.concrete_fine_collection import (
    ConcreteFineCollection,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.raw_material_for_clinker import (
    RawMaterialForClinker,  # demandreductioncircularity
)
from zen_europe.elements.retrofitting_technologies.biomass_to_cement_fuel import (
    BiomassToCementFuel,
)
from zen_europe.elements.retrofitting_technologies.cement_post_comb import (
    CementPostComb,
)
from zen_europe.elements.retrofitting_technologies.coal_to_cement_fuel import (
    CoalToCementFuel,
)
from zen_europe.elements.retrofitting_technologies.hydrogen_to_cement_fuel import (
    HydrogenToCementFuel,
)
from zen_europe.elements.retrofitting_technologies.waste_to_cement_fuel import (
    WasteToCementFuel,
)


class CementSector(Sector):
    """Cement clinker production."""
    # demandreductioncircularity: extended with cement, concrete and concrete recycling

    name = "cement"
    required_sectors = []

    def __init__(self) -> None:
        super().__init__()
        self.elements = [
            CementKiln,
            CoalToCementFuel,
            WasteToCementFuel,
            BiomassToCementFuel,
            HydrogenToCementFuel,
            CementPostComb,
            Clinker,
            FuelForCement,
            # demandreductioncircularity: new cement and concrete chain elements
            Cement,
            Concrete,
            ConcreteUse,
            ConcreteWaste,
            ConcreteFine,
            RawMaterialClinker,
            ClinkerInputMaterial,
            ClinkerToCement,
            CementToConcrete,
            ConcreteDemolishmentOverproduction,
            ConcreteFineCollection,
            CementRecycling,
            RawMaterialForClinker,
            CementFinesForClinker,
        ]
