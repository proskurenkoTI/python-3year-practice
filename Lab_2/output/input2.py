@dataclass
class FilmRecord:
    filmId: float
    filmTitle: str
    filmMaker: str
    productionYear: float
    scoreValue: float

@dataclass
class PerformerData:
    performerId: float
    performerName: str
    performerAge: float
    filmographyCount: float

def generateFilm(filmIdentifier: float, motionPictureTitle: str, directorName: str, yearOfRelease: float) -> FilmRecord:
    return {
    filmId: filmIdentifier,
    filmTitle: motionPictureTitle,
    filmMaker: directorName,
    productionYear: yearOfRelease,
    scoreValue: 0
    }

def generatePerformer(performerIdentifier: float, actorName: str, actorAge: float) -> PerformerData:
    return {
    performerId: performerIdentifier,
    performerName: actorName,
    performerAge: actorAge,
    filmographyCount: 0
    }

def modifyScore(filmData: FilmRecord, updatedScore: float) -> FilmRecord:
    filmData.scoreValue = updatedScore
    return filmData

checkIfOldFilm = lambda filmItem: filmItem.productionYear < 1980  # type: (FilmRecord) -> bool

def outputFilmTitle(filmRecord: FilmRecord) -> None:
    print(filmRecord.filmTitle)

def outputPerformerDetails(actorRecord: PerformerData) -> None:
    print(f"Performer: ${actorRecord.performerName}, Age: {actorRecord.performerAge}")

def incrementFilmCount(actorInfo: PerformerData) -> PerformerData:
    actorInfo.filmographyCount = actorInfo.filmographyCount + 1
    return actorInfo