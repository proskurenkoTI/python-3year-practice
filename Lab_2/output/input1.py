@dataclass
class PersonData:
    personId: float
    personName: str
    contactEmail: str
    yearsOld: float
    accountActive: bool

@dataclass
class ItemForSale:
    itemId: float
    itemName: str
    costValue: float

def makeNewPerson(identificationNumber: float, givenName: str, electronicMail: str, ageInYears: float) -> PersonData:
    return {
    personId: identificationNumber,
    personName: givenName,
    contactEmail: electronicMail,
    yearsOld: ageInYears,
    accountActive: True
    }

def computePriceReduction(baseCost: float, reductionPercent: float) -> float:
    return baseCost - baseCost * reductionPercent / 100

checkIfLegalAge = lambda ageValue: ageValue >= 18  # type: (float) -> bool

raiseCostByTen = lambda originalCost: originalCost + 10  # type: (float) -> float

def displayPersonName(personRecord: PersonData) -> None:
    print(personRecord.personName)