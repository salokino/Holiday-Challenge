# Holiday-Challenge

## About

This repository contains my submission for the CHECK24 TechUp Holiday Challenge, developed by Nikolas Witt. I created this project as part of the Check24 TechUp Holiday Challenge. This README contains all the important information.



## Demo

A short video demonstrating the application's features can be viewed here:

[Google Drive](https://drive.google.com/file/d/1dBATqeANcLOWvBA2X9qRkGIhaaUNA1Hg/view?usp=sharing)



## Features

- **fast hotel search:** find unique hotels with their cheapest offer based on multiple filter criteria
- **filter criteria:**
  - number of travelers (adults and children)
  - duration of the holiday
  - earliest departure date
  - latest return date
  - 49 airports including their real name
- **basic input validation:** ensure logical consistency (for example, if a user selects the earliest departure date, the latest return date must be after this date and must conform to the trip duration)
- **sort options:**
  - hotel name
  - price ascending
  - price descending
- **fast offers search:** find all the offers that a hotel provides based on the same filter criteria as above
- **sort all offers of a hotel** by
  - departure date ascending
  - departure date descending
  - price ascending
  - price descending
- **real flight durations**
- **option to view all hotels**



## Architecture

### Data Import Workflow

Firstly, there is the dataset. I have inspected the columns and the values they contain. Before importing the data to my PostgreSQL database, I created an object-relational mapping using SqlAlchemy. The classes can be found in [models.py](https://github.com/salokino/Holiday-Challenge/blob/main/src/backend/models.py). To optimise performance, I tried to use the minimum possible data type and added some validation methods. For example, the IATA airport code must be 3 characters long.

To import the data into my PostgreSQL database, I wrote an import script [import_data.py](https://github.com/salokino/Holiday-Challenge/blob/main/src/backend/import_data.py). As offers.csv is quite large, I loaded the data in chunks.

This concludes the data import process for the given datasets.



I've got some ideas for features during the implementation of the frontend and backend. I created the [IATA_codes.py](https://github.com/salokino/Holiday-Challenge/blob/main/src/backend/IATA_codes.py) script, which scrapes all the airport names corresponding to the given IATA codes from the offers.csv file on Wikipedia and stores them in a new CSV file. This CSV file is also imported into my database.

Furthermore, I noticed some inconsistencies in the provided data. The arrival times were correct, but the departure times were set to midnight, meaning the flight time to Mallorca was around 12 hours. To provide the user with the greatest possible accuracy, I created another script, [flight_durations.py](https://github.com/salokino/Holiday-Challenge/blob/main/src/backend/flight_durations.py), which scrapes flight durations from real flights between all the airports in the 'offers.csv' file and the airport in Mallorca. I then executed the following two queries to update the departure times of each offer.

#### Update Departure Times

##### Outbound flights

```sql
UPDATE offers o
SET
    outbound_departure_datetime = o.outbound_arrival_datetime - (fd.duration * INTERVAL '1 minute')
FROM
    flight_durations fd
WHERE
    o.outbound_departure_airport = fd.departure_airport
    AND o.outbound_arrival_airport = fd.arrival_airport;
```

##### Inbound flights

```sql
UPDATE offers o
SET
    inbound_departure_datetime = o.inbound_arrival_datetime - (fd.duration * INTERVAL '1 minute')
FROM
    flight_durations fd
WHERE
    o.inbound_departure_airport = fd.departure_airport
    AND o.inbound_arrival_airport = fd.arrival_airport;
```



### Backend

My business logic is contained within the [query_builder.py](https://github.com/salokino/Holiday-Challenge/blob/main/src/backend/query_builder.py) file. Using SQLAlchemy's syntax, it dynamically builds complex SQL queries based on user-provided filter criteria. The query builder classes hide the details of the database schema and query logic from the API endpoints. The query builder contains sophisticated filtering methods for dates, times of day, numeric ranges, and list inclusion. One of my goals was to create highly efficient queries. I achieved this by using modern concepts such as "Common Table Expressions" and indexes. See below for more information on indexes.

The api endpoints are defined in [main.py](https://github.com/salokino/Holiday-Challenge/blob/main/src/backend/main.py). They use important FastApi concepts, such as dependencies and query parameter objects. I had to configure the Cross-Origin Resource Sharing to allow my frontend application to interact with the API.



#### Indexes

I've created multiple indexes, but the important ones are:

| Index name                           | Index                                                        |
| ------------------------------------ | ------------------------------------------------------------ |
| idx_offers_cheapest_search           | CREATE INDEX idx_offers_cheapest_search ON public.offers USING btree (duration, count_adults, count_children, hotel_id, price, offer_id, outbound_departure_airport) |
| idx_offers_cheapest_search_with_date | CREATE INDEX idx_offers_cheapest_search_with_date ON public.offers USING btree (duration, count_adults, count_children, hotel_id, price, offer_id, outbound_departure_airport, outbound_departure_datetime, inbound_departure_datetime) |
| idx_offers_departure_datetime_asc    | CREATE INDEX idx_offers_departure_datetime_asc ON public.offers USING btree (hotel_id, outbound_departure_datetime) |

#### API endpoints

- **/airports**: returns the airports including their iata_code and name
- **/available-hotels**: return all available hotels and offers to filter by number of stars
- **/flight-details/{offer_id}**: get the flight details of a specific offer by its id (airports, arrival & departure times)
- **/offers/{hotel_id}**: get all the offers of a hotel respecting the filter options
- **/hotels**: get the cheapest offer of a hotel respecting the filter options



### Frontend

I've created the frontend from scratch. Therefore I've leveraged my nextjs knowledge and build a user friendly, clean, nice-looking but simple web application. I tried to keep edge cases in mind when the user interacts with the application, such as input validation methods.



## Tech Stack

- **Backend:** Python, FastAPI, BeautifulSoup, SQLAlchemy, Pydantic
- **Database:** PostgreSQL
- **Frontend:** Nextjs, Typescript



## Getting Started (pretty basic)

To get started, the datasets must be in a folder called 'data', two directories above the location of the scrips:

| root

| ---- data

​	| ---- hotels.csv

​	| ---- offers.csv

| ---- src

​	| ---- backend

​		| ---- import_data.py

​		| ---- utils.py

​		| ---- flight_durations.py

​		etc

​	| ---- frontend



### Python Libraries

- beautifulsoup4==4.13.4
- fastapi==0.116.1
- pandas==2.3.1
- psycopg2==2.9.10
- pydantic==2.11.7
- requests==2.32.4
- SQLAlchemy==2.0.42



### Database import

In order to import the data to a postgres database, create a .env file with the following content:

``````
DB_NAME=<db-name>
HOST="127.0.0.1"
PASSWORD=<password>
PORT=5432
USER=<user>
``````



in order to import the data, you need the airports.csv. You can copy it from the data directory or by running [this file](https://github.com/salokino/Holiday-Challenge/blob/main/src/backend/IATA_codes.py).



### Backend

- inside the backend directory run:

```python
fastapi run dev
```



### Frontend

- inside the frontend directory run:

```python
npm install
npm run dev
```



PS: I know that this is a rough getting started, and not a good one either. If you want to get it running and have difficulties, feel free to reach out. I'm very happy to help.



## Possible Improvements

If I had more time, I would consider adding the following features and improvements (some of which already exist in part):

- using Redis as a cache to speed up frequently used queries
- implement the remaining filter options in the frontend (the backend already covers the functionality) such as:
  - price: minimum and maximum price
  - flight details: arrival and departure times (day, afternoon, evening, night)
  - mealtype
  - roomtype
  - etc
- add images of the hotels and links to their websites
- add a text search
- add the functionality to save offers
