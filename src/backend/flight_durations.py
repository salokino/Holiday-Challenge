from bs4 import BeautifulSoup
import re
import requests

# von-pmi-nach-lgg
URL = "https://www.flightconnections.com/de/fl%C3%BCge-von-"

airports = [
  "HHN", "HAM", "MUC", "PRG", "HAJ", "CRL", "LUX", "DTM", "NRN", "LBC", "BLL",
  "DUS", "RLG", "EIN", "KSF", "BRN", "GVA", "KRK", "VIE", "KLU", "FDH", "FMO",
  "BER", "NUE", "FMM", "SCN", "WAW", "SXB", "GWT", "LGG", "PAD", "DRS", "ZRH",
  "LNZ", "CSO", "FKB", "SZG", "CGN", "AMS", "GRZ", "LEJ", "BRU", "STR", "ERF",
  "FRA", "BSL", "BRE", "INN"
]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_duration_in_minutes(duration: str) -> int:
  # duration looks like 2 Stunden und 20 Minuten

  duration_splitted = duration.split(" ")

  hours = int(duration_splitted[0])
  if len(duration_splitted) == 2:
    return hours * 60

  if len(duration_splitted) == 5:
    minutes = int(duration_splitted[3])

    # one hour has 60 minutes -> 1h = 60min
    duration_in_minutes = hours * 60 + minutes

    return  duration_in_minutes

  return 0


def get_flight_data(
    arrival_airport, departure_airport: str,
    default_duration: str = "0 Stunden und 0 Minuten") -> str:

  page = requests.get(url=f"{URL}{departure_airport}-nach-{arrival_airport}", headers=headers)
  soup = BeautifulSoup(markup=page.text, features="html")
  
  for row in soup.find_all("div", {"class": "route-page-info-text"}):
    entry = str(row)

    if re.search(pattern="(\\d (Stunde|Stunden) und \\d{1,2} Minuten)|(\\d (Stunde|Stunden))", string=entry):
      match_soup = BeautifulSoup(markup=entry, features="html")
      duration = match_soup.find(name="span")

      if duration:
        return duration.text


  return default_duration


def store_flight_durations(data: list[str]) -> None:
  with open("flight_durations.csv", "w") as file:
    for row in data:
      file.write(f"{row}\n")


if __name__ == "__main__":
  holiday_airport = "PMI"

  data = ["departure_airport,arrival_airport,minutes"]

  for airport in airports:
    outbound_duration = get_flight_data(departure_airport=airport, arrival_airport=holiday_airport)
    inbound_duration = get_flight_data(departure_airport=holiday_airport,  arrival_airport=airport)

    outbound_duration_in_minutes = get_duration_in_minutes(duration=outbound_duration)
    inbound_duration_in_minutes = get_duration_in_minutes(duration=inbound_duration)

    data.append(f"{airport},{holiday_airport},{outbound_duration_in_minutes}")
    data.append(f"{holiday_airport},{airport},{inbound_duration_in_minutes}")


  store_flight_durations(data=data)