from zen_creator import Sector

from zen_europe.elements.carriers.methanol import Methanol
from zen_europe.elements.carriers.non_plastic_olefins import (
    NonPlasticOlefins,  # demandreductioncircularity
)
from zen_europe.elements.carriers.olefin import Olefin
from zen_europe.elements.carriers.plastic import Plastic  # demandreductioncircularity
from zen_europe.elements.carriers.plastic_use import (
    PlasticUse,  # demandreductioncircularity
)
from zen_europe.elements.carriers.plastic_waste import (
    PlasticWaste,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.chemical_recycling_plastic import (
    ChemicalRecyclingPlastic,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.incineration_plastic import (
    IncinerationPlastic,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.mechanical_recycling_plastic import (
    MechanicalRecyclingPlastic,  # demandreductioncircularity
)

from zen_europe.elements.conversion_technologies.methanol_from_biomass import (
    MethanolFromBiomass,
)
from zen_europe.elements.conversion_technologies.methanol_from_hydrogen import (
    MethanolFromHydrogen,
)
from zen_europe.elements.conversion_technologies.methanol_from_natural_gas import (
    MethanolFromNaturalGas,
)
from zen_europe.elements.conversion_technologies.methanol_ICE_ship import (
    MethanolICEShip,
)
from zen_europe.elements.conversion_technologies.olefin_from_methanol import (
    OlefinFromMethanol,
)
from zen_europe.elements.conversion_technologies.olefin_from_naphtha import (
    OlefinFromNaphtha,
)
from zen_europe.elements.conversion_technologies.olefins_to_nonplastics import (
    OlefinsToNonplastics,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.overproduction_use_plastic import (
    OverproductionUsePlastic,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.polymerisation import (
    Polymerisation,  # demandreductioncircularity
)
from zen_europe.elements.transport_technologies.methanol_pipeline import (
    MethanolPipeline,
)
from zen_europe.elements.transport_technologies.olefin_pipeline import OlefinPipeline


class MethanolSector(Sector):
    """Methanol and olefin production and transport."""
    # demandreductioncircularity: extended with plastic production, use and recycling
    name = "methanol"
    required_sectors = [
        "electricity",
        "district_heating",
        "hydrogen",
        "refining",
        "gas",
        "heat",  # demandreductioncircularity: heat input of polymerisation
    ]

    def __init__(self) -> None:
        super().__init__()
        self.elements = [
            MethanolFromNaturalGas,
            MethanolFromBiomass,
            OlefinFromMethanol,
            MethanolPipeline,
            OlefinPipeline,
            MethanolFromHydrogen,
            OlefinFromNaphtha,
            MethanolICEShip,
            Methanol,
            Olefin,
            # demandreductioncircularity: new plastics chain elements
            Plastic,
            PlasticUse,
            PlasticWaste,
            NonPlasticOlefins,
            Polymerisation,
            OverproductionUsePlastic,
            MechanicalRecyclingPlastic,
            ChemicalRecyclingPlastic,
            IncinerationPlastic,
            OlefinsToNonplastics,
        ]
