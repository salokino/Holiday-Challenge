const getMealtypeIconFilename = (mealtype: string) => {
  switch (mealtype) {
    case 'accordingdescription':
      return 'according_description.svg';
    case 'allinclusive':
    case 'allinclusivelight':
    case 'allinclusiveplus':
      return 'all_inclusive.svg';
    case 'breakfast':
      return 'breakfast.svg';
    case 'fullboard':
    case 'fullboardplus':
      return 'fullboard.svg';
    case 'halfboard':
    case 'halfboardplus':
      return 'halfboard.svg';
    case 'program':
      return 'program.svg';
    case 'selfcatering':
      return 'self_catering.svg';
    default:
      return 'no_food.svg';
  }
};

const getRoomtypeIconFilename = (roomtype: string) => {
  switch (roomtype) {
    case 'apartment':
      return 'apartment.svg';
    case 'bungalow':
      return 'bungalow.svg';
    case 'double':
      return 'double_bed.svg';
    case 'family':
      return 'family.svg';
    case 'fourbedroom':
      return 'fourbedroom.svg';
    case 'holidayflat':
      return 'holiday_flat.svg';
    case 'juniorsuite':
    case 'suite':
      return 'suite.svg';
    case 'program':
      return 'program.svg';
    case 'single':
      return 'single_bed.svg';
    case 'studio':
      return 'studio.svg';
    case 'triple':
      return 'triple.svg';
    case 'twinroom':
      return 'twinroom.svg';
    case 'unknown':
      return 'unknown.svg';
    case 'villa':
      return 'villa.svg';
  }
};

export { getMealtypeIconFilename, getRoomtypeIconFilename };
