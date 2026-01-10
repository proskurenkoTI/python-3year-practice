interface FilmRecord {
  filmId: number;
  filmTitle: string;
  filmMaker: string;
  productionYear: number;
  scoreValue: number;
}

interface PerformerData {
  performerId: number;
  performerName: string;
  performerAge: number;
  filmographyCount: number;
}

function generateFilm(
  filmIdentifier: number,
  motionPictureTitle: string,
  directorName: string,
  yearOfRelease: number
): FilmRecord {
  return {
    filmId: filmIdentifier,
    filmTitle: motionPictureTitle,
    filmMaker: directorName,
    productionYear: yearOfRelease,
    scoreValue: 0
  };
}

function generatePerformer(
  performerIdentifier: number,
  actorName: string,
  actorAge: number
): PerformerData {
  return {
    performerId: performerIdentifier,
    performerName: actorName,
    performerAge: actorAge,
    filmographyCount: 0
  };
}

function modifyScore(
  filmData: FilmRecord,
  updatedScore: number
): FilmRecord {
  return {
    ...filmData,
    scoreValue: updatedScore
  };
}

const checkIfOldFilm = (filmItem: FilmRecord): boolean => filmItem.productionYear < 1980;
const verifyAdultPerformer = (performerItem: PerformerData): boolean => performerItem.performerAge >= 18;

const outputFilmTitle = (filmRecord: FilmRecord): void => {
  console.log(filmRecord.filmTitle);
};

const outputPerformerDetails = (actorRecord: PerformerData): void => {
  console.log(`Performer: ${actorRecord.performerName}, Age: ${actorRecord.performerAge}`);
};

function incrementFilmCount(actorInfo: PerformerData): PerformerData {
  return {
    ...actorInfo,
    filmographyCount: actorInfo.filmographyCount + 1
  };
}