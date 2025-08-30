const getFormattedDate = (date: string) => {
  const dateAsDate = new Date(date);
  const day = dateAsDate.getDate();
  const month = dateAsDate.toLocaleString('default', { month: 'short' });
  const year = dateAsDate.getFullYear();

  return `${day} ${month} ${year}`;
};

const getFormattedTime = (date: string) => {
  const dateAsDate = new Date(date);
  const hours = dateAsDate.getHours();
  const minutes = dateAsDate.getMinutes();

  // Add leading zeros
  const hoursAsString = hours < 10 ? `0${hours}` : hours;
  const minutesAsString = minutes < 10 ? `0${minutes}` : minutes;

  return `${hoursAsString}:${minutesAsString}`;
};

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

const getTimeDifference = (
  arrivalDatetime: string,
  departureDatetime: string
) => {
  const arrivalDate = new Date(arrivalDatetime);
  const departureDate = new Date(departureDatetime);

  const differenceInHours =
    Math.abs(arrivalDate.getTime() - departureDate.getTime()) / 36e5;
  const hours = Math.floor(differenceInHours);
  const minutes = Math.round((differenceInHours - hours) * 60);
  return `${hours} ${hours !== 1 ? 'hours' : 'hour'} and ${minutes} ${
    minutes !== 1 ? 'minutes' : 'minute'
  }`;
};

const transformDate = (date: Date) => {
  // transform date to yyyy-mm-dd
  const day = date.getDate();
  const month = date.getMonth();
  const year = date.getFullYear();

  // add leading zeros
  const dayAsString = day < 10 ? `0${day}` : day;
  const monthAsString = month + 1 < 10 ? `0${month + 1}` : month + 1;

  return `${year}-${monthAsString}-${dayAsString}`;

  return;
};

export {
  getFormattedDate,
  getFormattedTime,
  getMealtypeIconFilename,
  getRoomtypeIconFilename,
  getTimeDifference,
  transformDate,
};
