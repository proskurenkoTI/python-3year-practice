interface VehicleInfo {
  manufacturer: string;
  vehicleModel: string;
  manufactureYear: number;
  vehiclePrice: number;
  isBrandNew: boolean;
}

interface VehicleOwner {
  ownerName: string;
  ownerAge: number;
  vehiclesOwned: number;
}

function welcomeOwner(ownerIdentifier: string): void {
  console.log(`Welcome, ${ownerIdentifier}!`);
}

function computeValueLoss(
  automobile: VehicleInfo,
  yearsPassed: number
): number {
  const depreciationAmount = automobile.vehiclePrice * 0.1 * yearsPassed;
  const finalValue = automobile.vehiclePrice - depreciationAmount;
  return finalValue;
}

function generateVehicle(
  brandName: string,
  modelType: string,
  yearMade: number,
  initialPrice: number
): VehicleInfo {
  return {
    manufacturer: brandName,
    vehicleModel: modelType,
    manufactureYear: yearMade,
    vehiclePrice: initialPrice,
    isBrandNew: true
  };
}

function adjustVehicleCost(
  carData: VehicleInfo,
  priceCut: number
): VehicleInfo {
  const modifiedVehicle = {
    manufacturer: carData.manufacturer,
    vehicleModel: carData.vehicleModel,
    manufactureYear: carData.manufactureYear,
    vehiclePrice: carData.vehiclePrice - priceCut,
    isBrandNew: carData.isBrandNew
  };
  console.log(`Price adjusted for: ${carData.vehicleModel}`);
  return modifiedVehicle;
}

const checkIfHistoricVehicle = (automobile: VehicleInfo): boolean => {
  return automobile.manufactureYear < 1990;
};

const vehicleCollection = [
  { manufacturer: "Toyota", vehicleModel: "Camry", manufactureYear: 2020, vehiclePrice: 25000, isBrandNew: true },
  { manufacturer: "Ford", vehicleModel: "Mustang", manufactureYear: 1967, vehiclePrice: 45000, isBrandNew: false }
];

const ownerList = [
  { ownerName: "John", ownerAge: 35, vehiclesOwned: 2 },
  { ownerName: "Sarah", ownerAge: 28, vehiclesOwned: 1 }
];

const increaseVehiclePrice = (carInfo: VehicleInfo): VehicleInfo => {
  return {
    ...carInfo,
    vehiclePrice: carInfo.vehiclePrice + 1000
  };
};

function createDefaultVehicle(): VehicleInfo {
  return {
    manufacturer: "Unknown",
    vehicleModel: "Unknown",
    manufactureYear: 2000,
    vehiclePrice: 0,
    isBrandNew: false
  };
}