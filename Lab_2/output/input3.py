@dataclass
class VehicleInfo:
    manufacturer: str
    vehicleModel: str
    manufactureYear: float
    vehiclePrice: float
    isBrandNew: bool

@dataclass
class VehicleOwner:
    ownerName: str
    ownerAge: float
    vehiclesOwned: float

def welcomeOwner(ownerIdentifier: str) -> None:
    print(f"Welcome, {ownerIdentifier}not ")

def computeValueLoss(automobile: VehicleInfo, yearsPassed: float) -> float:
    depreciationAmount = automobile.vehiclePrice * 0.1 * yearsPassed
    finalValue = automobile.vehiclePrice - depreciationAmount
    return finalValue

def generateVehicle(brandName: str, modelType: str, yearMade: float, initialPrice: float) -> VehicleInfo:
    return {
    manufacturer: brandName,
    vehicleModel: modelType,
    manufactureYear: yearMade,
    vehiclePrice: initialPrice,
    isBrandNew: True
    }

def adjustVehicleCost(carData: VehicleInfo, priceCut: float) -> VehicleInfo:
    modifiedVehicle = {
    manufacturer: carData.manufacturer,
    vehicleModel: carData.vehicleModel,
    manufactureYear: carData.manufactureYear,
    vehiclePrice: carData.vehiclePrice - priceCut,
    isBrandNew: carData.isBrandNew
    }
    print(f"Price adjusted for: {carData.vehicleModel}")
    return modifiedVehicle

def checkIfHistoricVehicle(automobile: VehicleInfo) -> bool:
    return automobile.manufactureYear < 1990

vehicleCollection = [
  { manufacturer: "Toyota", vehicleModel: "Camry", manufactureYear: 2020, vehiclePrice: 25000, isBrandNew: True },
  { manufacturer: "Ford", vehicleModel: "Mustang", manufactureYear: 1967, vehiclePrice: 45000, isBrandNew: False }
]

ownerList = [
  { ownerName: "John", ownerAge: 35, vehiclesOwned: 2 },
  { ownerName: "Sarah", ownerAge: 28, vehiclesOwned: 1 }
]

def increaseVehiclePrice(carInfo: VehicleInfo) -> VehicleInfo:
    carInfo.vehiclePrice = carInfo.vehiclePrice + 1000
    return carInfo

def createDefaultVehicle() -> VehicleInfo:
    return {
    manufacturer: "Unknown",
    vehicleModel: "Unknown",
    manufactureYear: 2000,
    vehiclePrice: 0,
    isBrandNew: False
    }