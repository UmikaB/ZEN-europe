from zen_creator import Sector
from zen_europe.elements.carriers.bus_mileage import (  # demandreductioncircularity
    BusMileage,
)
from zen_europe.elements.carriers.diesel import Diesel
from zen_europe.elements.carriers.gasoline import Gasoline
from zen_europe.elements.carriers.passenger_mileage import PassengerMileage
from zen_europe.elements.carriers.regional_transport import (
    RegionalTransport,  # demandreductioncircularity
)
from zen_europe.elements.carriers.train_mileage import (  # demandreductioncircularity
    TrainMileage,
)
from zen_europe.elements.carriers.tram_metro_mileage import (
    TramMetroMileage,  # demandreductioncircularity
)
from zen_europe.elements.carriers.urban_transport import (  # demandreductioncircularity
    UrbanTransport,
)
from zen_europe.elements.conversion_technologies.BEV import BEV
from zen_europe.elements.conversion_technologies.bus_BEV import (
    Bus_BEV,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.bus_ICE_diesel import (
    Bus_ICE_diesel,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.bus_to_urban import (
    BusToUrban,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.car_passenger_mileage_to_regional import (
    CarPassengerMileageToRegional,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.car_passenger_mileage_to_urban import (
    CarPassengerMileageToUrban,  # demandreductioncircularity
)

from zen_europe.elements.conversion_technologies.ICE_diesel import ICE_diesel
from zen_europe.elements.conversion_technologies.ICE_petrol import ICE_petrol
from zen_europe.elements.conversion_technologies.train import (
    Train,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.train_passenger_mileage_to_regional import (
    TrainPassengerMileageToRegional,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.tram_metro import (
    TramMetro,  # demandreductioncircularity
)
from zen_europe.elements.conversion_technologies.tram_metro_to_urban import (
    TramMetroToUrban,  # demandreductioncircularity
)
from zen_europe.elements.storage_technologies.BEV_buffer import (
    BEVBuffer,  # demandreductioncircularity
)
from zen_europe.elements.storage_technologies.BusBEV_buffer_urban import (
    BusBEVBufferUrban,  # demandreductioncircularity
)

class PassengerTransportSector(Sector):
    """Passenger vehicle transport demand.

     demandreductioncircularity: urban and regional passenger transport, met by
    cars, buses, trams/metros and trains
    """

    name = "passenger_transport"
    required_sectors = ["electricity"]

    def __init__(self) -> None:
        super().__init__()
        self.elements = [
            BEV,
            ICE_diesel,
            ICE_petrol,
            Gasoline,
            Diesel,
            PassengerMileage,
            # demandreductioncircularity: passenger transport chain
            UrbanTransport,
            RegionalTransport,
            BusMileage,
            TramMetroMileage,
            TrainMileage,
            Bus_ICE_diesel,
            Bus_BEV,
            TramMetro,
            Train,
            CarPassengerMileageToUrban,
            CarPassengerMileageToRegional,
            BusToUrban,
            TramMetroToUrban,
            TrainPassengerMileageToRegional,
            BEVBuffer,
            BusBEVBufferUrban,
        ]
