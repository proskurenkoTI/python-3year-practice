interface PersonData {
  personId: number;
  personName: string;
  contactEmail: string;
  yearsOld: number;
  accountActive: boolean;
}

interface ItemForSale {
  itemId: number;
  itemName: string;
  costValue: number;
}

function makeNewPerson(
  identificationNumber: number,
  givenName: string,
  electronicMail: string,
  ageInYears: number
): PersonData {
  return {
    personId: identificationNumber,
    personName: givenName,
    contactEmail: electronicMail,
    yearsOld: ageInYears,
    accountActive: true
  };
}

function computePriceReduction(
  baseCost: number,
  reductionPercent: number
): number {
  return baseCost - baseCost * reductionPercent / 100;
}

const checkIfLegalAge = (ageValue: number): boolean => ageValue >= 18;

const raiseCostByTen = (originalCost: number): number => originalCost + 10;

const displayPersonName = (personRecord: PersonData): void => {
  console.log(personRecord.personName);
};