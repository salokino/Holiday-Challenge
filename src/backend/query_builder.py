# pyright: reportAttributeAccessIssue=false

from datetime import datetime, time
from functools import partial
from models import Airport, Hotel, Offer
from schemas import HotelsSearchQueryBasic, HotelsSearchQueryAdvanced
from sqlalchemy import select, Select, func, Selectable
from sqlalchemy.orm import InstrumentedAttribute, aliased

import operator


class AirportQueryBuilder:
    def __init__(self) -> None:
        pass

    def get_airports(self) -> Select:
        query = select(
            Airport.iata_code,
            Airport.name
        ).order_by(Airport.name)

        return query

    def get_flight_details(self, offer_id: int) -> Select:
        departure_airport = aliased(Airport)
        arrival_airport = aliased(Airport)

        query = select(
            departure_airport.name.label("outbound_departure_name"),
            arrival_airport.name.label("outbound_arrival_name"),
            Offer.inbound_arrival_airport,
            Offer.inbound_arrival_datetime,
            Offer.inbound_departure_airport,
            Offer.inbound_departure_datetime,
            Offer.outbound_arrival_airport,
            Offer.outbound_arrival_datetime,
            Offer.outbound_departure_airport,
            Offer.outbound_departure_datetime
        ).join(
            departure_airport,
            Offer.outbound_departure_airport == departure_airport.iata_code
        ).join(
            arrival_airport,
            Offer.outbound_arrival_airport == arrival_airport.iata_code
        ).where(
            Offer.offer_id == offer_id
        )

        return query


class BaseQueryBuilder:
    def __init__(self, query_params: HotelsSearchQueryBasic) -> None:
        self.query_params = query_params

        self._schema_attribute_mapping = {
            "adults": Offer.count_adults,
            "airport": Offer.outbound_departure_airport,
            "children": Offer.count_children,
            "duration": Offer.duration,
            "earliest_departure": Offer.outbound_departure_datetime,
            "latest_return": Offer.inbound_departure_datetime,
        }

        self._parameter_filter_mapping = {
            "adults": self._generic_equals_filter,
            "airport": self._airport_filter ,
            "children": self._generic_equals_filter,
            "duration": self._generic_equals_filter,
            "earliest_departure": partial(self._date_comparison_filter, op=operator.ge),
            "latest_return": partial(self._date_comparison_filter, op=operator.le),
        }

    def _airport_filter(self, attribute: InstrumentedAttribute, query: Select, value) -> Select:
        return query.where(attribute.in_(value))

    def _date_comparison_filter(self, attribute: InstrumentedAttribute, query: Select, value, op) -> Select:
        """
        Applies a date comparison filter to the given attribute. The date is converted to a datetime
        at the start of the day for greater than or equal comparisons and at the end of the day for
        less than or equal comparisons.

        Parameters
        ----------
        attribute : InstrumentedAttribute
            The attribute to be filtered.
        query : Select
            The query to be filtered.
        value : date
            The date to filter by.
        op: Operator
            The comparison operator to use. Must be either operator.ge or operator.le.

        Returns
        -------
        Select
            The filtered query.
        """

        if op == operator.ge:
            # date at start of day in datetime format
            datetime_value = datetime.combine(value, time.min)

        # op == operator.le
        else:
            # date at end of day in datetime format
            datetime_value = datetime.combine(value, time.max)

        return query.where(op(attribute, datetime_value))

    def _extract_non_null_query_params(self) -> dict[str, str]:
        """
        Extracts the non-null query parameters from the query_params object.

        Returns
        -------
        dict[str, str]
            A dictionary containing the non-null query parameters.
        """

        selected_parameters = dict(filter(lambda param: param[1] is not None, self.query_params))
        return selected_parameters

    def _filter_all_offers(self, query: Select) -> Selectable:
        """ Applies all filters to the Offer table based on the query parameters the user provided.

        Returns
        -------
        Selectable
            A CTE containing all offers that match the given query parameters.
        """

        non_null_params = self._extract_non_null_query_params()
        for param in non_null_params:
            attribute = self._schema_attribute_mapping[param]
            query = self._parameter_filter_mapping[param](attribute=attribute, query=query, value=non_null_params[param])

        return query.cte("filtered_offers")

    def _generic_comparison_filter(self, attribute: InstrumentedAttribute, query: Select, value, op) -> Select:
        """
        Generic filter that applies a comparison filter to the given attribute.

        Parameters
        ----------
        attribute : InstrumentedAttribute
            The attribute to be filtered.
        query : Select
            The query to be filtered.
        value : Any
            The value to filter by.
        op: Operator
            The comparison operator to use.

        Returns
        -------
        Select
            The filtered query.
        """

        return query.where(op(attribute, value))

    def _generic_equals_filter(self, attribute: InstrumentedAttribute, query: Select, value) -> Select:
        """
        Generic filter that applies an equality filter to the given attribute.

        Parameters
        ----------
        attribute : InstrumentedAttribute
            The attribute to be filtered.
        query : Select
            The query to be filtered.
        value : Any
            The value to filter by.

        Returns
        -------
        Select
            The filtered query.
        """

        return query.where(attribute == value)

    # TODO: make this method sargable
    def _time_filter(self, attribute: InstrumentedAttribute, query: Select, value) -> Select:
        """ Filters the query based on the time of day. The time of day is divided into four intervals:
        - morning: 6am - 12pm
        - afternoon: 12pm - 6pm
        - evening: 6pm - 10pm
        - night: 10pm - 6am

        Parameters
        ----------
        attribute : InstrumentedAttribute
            The attribute to be filtered.
        query : Select
            The query to be filtered.
        value : str
            The time of day to filter by. Must be one of "morning", "afternoon", "evening", "night".

        Returns
        -------
        Select
            The filtered query.
        """

        time_intervals = {
            "morning": (6,12),
            "afternoon": (12,18),
            "evening": (18,22),
            "night": (22,6)
        }

        lower_limit = time_intervals[value][0]
        upper_limit = time_intervals[value][1]

        if value == "night":
            return query.where(
                (
                    # time between lower limit and midnight
                    (func.extract('hour', attribute) >= lower_limit) &
                    (func.extract("hour", attribute) < 24)
                ) |
                (
                    # time between midnight and upper limit
                    (func.extract('hour', attribute) >= 0) &
                    (func.extract("hour", attribute) < upper_limit)
                )
            )

        return query.where(
                (func.extract('hour', attribute) >= lower_limit) &
                (func.extract("hour", attribute) < upper_limit)
            )


class HotelOffersQueryBuilder(BaseQueryBuilder):
    def __init__(self, hotel_id: int, limit:int, offset: int, query_params: HotelsSearchQueryAdvanced) -> None:
        self.hotel_id = hotel_id
        self.limit = limit
        self.offset = offset
        self.query_params = query_params
        self._schema_attribute_mapping = {
            "adults": Offer.count_adults,
            "airport": Offer.outbound_departure_airport,
            "children": Offer.count_children,
            "duration": Offer.duration,
            "earliest_departure": Offer.outbound_departure_datetime,
            "inbound_arrival_time": Offer.inbound_arrival_datetime,
            "inbound_departure_time": Offer.inbound_departure_datetime,
            "latest_return": Offer.inbound_departure_datetime,
            "mealtype": Offer.mealtype,
            "oceanview": Offer.oceanview,
            "outbound_arrival_time": Offer.outbound_arrival_datetime,
            "outbound_departure_time": Offer.outbound_departure_datetime,
            "price_max": Offer.price,
            "price_min": Offer.price,
            "roomtype": Offer.roomtype
        }
        self._parameter_filter_mapping = {
            "adults": self._generic_equals_filter,
            "airport": self._airport_filter ,
            "children": self._generic_equals_filter,
            "duration": self._generic_equals_filter,
            "earliest_departure": partial(self._date_comparison_filter, op=operator.ge),
            "inbound_arrival_time": self._time_filter,
            "inbound_departure_time": self._time_filter,
            "latest_return": partial(self._date_comparison_filter, op=operator.le),
            "mealtype": self._generic_equals_filter,
            "oceanview": self._generic_equals_filter,
            "outbound_arrival_time": self._time_filter,
            "outbound_departure_time": self._time_filter,
            "price_max": partial(self._generic_comparison_filter, op=operator.le),
            "price_min": partial(self._generic_comparison_filter, op=operator.ge),
            "roomtype": self._generic_equals_filter
        }

    def build_query(self) -> Select:
        """
        Builds the query to get offers for a specific hotel based on the query parameters.

        Returns
        -------
        Select
            The query to get offers for the specified hotel matching the query parameters.
        """

        filtered_offers_cte = self._filter_all_offers(
            select(
                Offer.count_adults,
                Offer.count_children,
                Offer.duration,
                Offer.inbound_departure_datetime,
                Offer.mealtype,
                Offer.oceanview,
                Offer.offer_id,
                Offer.outbound_departure_datetime,
                Offer.price,
                Offer.roomtype)
        )

        query = select(
            Hotel.hotel_name,
            Hotel.hotel_stars,
            filtered_offers_cte.c.count_adults,
            filtered_offers_cte.c.count_children,
            filtered_offers_cte.c.duration,
            filtered_offers_cte.c.inbound_departure_datetime,
            filtered_offers_cte.c.mealtype,
            filtered_offers_cte.c.oceanview,
            filtered_offers_cte.c.offer_id,
            filtered_offers_cte.c.outbound_departure_datetime,
            filtered_offers_cte.c.price,
            filtered_offers_cte.c.roomtype
        ).join(
            target=Hotel,
            onclause=Hotel.hotel_id == self.hotel_id
        ).where(
            Hotel.hotel_id == self.hotel_id
        ).limit(self.limit).offset(self.offset)

        return query


class CheapestOffersQueryBuilder(BaseQueryBuilder):
    def __init__(self, query_params: HotelsSearchQueryAdvanced) -> None:
        self.query_params = query_params
        self._schema_attribute_mapping = {
            "adults": Offer.count_adults,
            "airport": Offer.outbound_departure_airport,
            "children": Offer.count_children,
            "duration": Offer.duration,
            "earliest_departure": Offer.outbound_departure_datetime,
            "inbound_arrival_time": Offer.inbound_arrival_datetime,
            "inbound_departure_time": Offer.inbound_departure_datetime,
            "latest_return": Offer.inbound_departure_datetime,
            "mealtype": Offer.mealtype,
            "oceanview": Offer.oceanview,
            "outbound_arrival_time": Offer.outbound_arrival_datetime,
            "outbound_departure_time": Offer.outbound_departure_datetime,
            "price_max": Offer.price,
            "price_min": Offer.price,
            "roomtype": Offer.roomtype
        }
        self._parameter_filter_mapping = {
            "adults": self._generic_equals_filter,
            "airport": self._airport_filter ,
            "children": self._generic_equals_filter,
            "duration": self._generic_equals_filter,
            "earliest_departure": partial(self._date_comparison_filter, op=operator.ge),
            "inbound_arrival_time": self._time_filter,
            "inbound_departure_time": self._time_filter,
            "latest_return": partial(self._date_comparison_filter, op=operator.le),
            "mealtype": self._generic_equals_filter,
            "oceanview": self._generic_equals_filter,
            "outbound_arrival_time": self._time_filter,
            "outbound_departure_time": self._time_filter,
            "price_max": partial(self._generic_comparison_filter, op=operator.le),
            "price_min": partial(self._generic_comparison_filter, op=operator.ge),
            "roomtype": self._generic_equals_filter
        }

    def _get_cheapest_offers(self, cte: Selectable) -> Selectable:
        """ Returns a CTE that contains the cheapest offer per hotel from the given CTE.

        Parameters
        ----------
        cte : Selectable
            A CTE containing the offers to be filtered.

        Returns
        -------
        Selectable
            A CTE containing the cheapest offer per hotel.
        """

        cheapest_offers_cte = select(
            cte.c.hotel_id,
            func.min(cte.c.price).label("min_price"),
            func.min(cte.c.offer_id).label("min_offer_id"),
        ).group_by(
            cte.c.hotel_id
        ).cte("cheapest_offers")

        return cheapest_offers_cte

    def _get_relevant_offer_details(self, cte: Selectable) -> Selectable:
        """ Returns a CTE that contains the relevant details of each offer.

        Returns
        -------
        Selectable
            A CTE containing the relevant details of each offer.
        """

        relevant_details_cte = select(
            cte.c.hotel_id,
            cte.c.min_price.label("price"),
            cte.c.min_offer_id,
            Offer.mealtype,
            Offer.roomtype,
            Offer.count_adults,
            Offer.count_children,
            Offer.duration,
            Hotel.hotel_name,
            Hotel.hotel_stars
        ).join(
            target=cte,
            onclause=Offer.offer_id == cte.c.min_offer_id
        ).join(
            target=Hotel,
            onclause=Offer.hotel_id==Hotel.hotel_id
        ).cte("relevant_offer_details")

        return relevant_details_cte

    def build_query(self) -> Select:
        """
        Builds the final query based on the given query parameters, which
        returns the cheapest offer per hotel along with the count of offers
        per hotel and trip details.

        Returns
        -------
        Select
            The final query.
        """

        filtered_offers_cte = self._filter_all_offers(query=select(Offer.hotel_id, Offer.offer_id, Offer.price))
        cheapest_offers_cte = self._get_cheapest_offers(cte=filtered_offers_cte)
        relevant_offer_details_cte = self._get_relevant_offer_details(cte=cheapest_offers_cte)

        final_query = select(
            relevant_offer_details_cte.c.hotel_id,
            relevant_offer_details_cte.c.mealtype,
            relevant_offer_details_cte.c.roomtype,
            relevant_offer_details_cte.c.count_adults,
            relevant_offer_details_cte.c.count_children,
            relevant_offer_details_cte.c.price,
            relevant_offer_details_cte.c.duration,
            relevant_offer_details_cte.c.hotel_name,
            relevant_offer_details_cte.c.hotel_stars
        )

        return final_query
