from datetime import datetime, time
from functools import partial
from models import Offer, Hotel
from schemas import HotelsSearchQueryAdvanced
from sqlalchemy import select, Select, func, Subquery, distinct
from sqlalchemy.orm import InstrumentedAttribute

import operator


class QueryBuilder:
    def __init__(self, query_params: HotelsSearchQueryAdvanced) -> None:
        self.query_params = query_params
        self.query = select(Offer)
        self._schema_attribute_mapping = {
            "adults": Offer.count_adults,
            "children": Offer.count_children,
            "duration": Offer.duration,
            "earliest_departure": Offer.inbound_departure_datetime,
            "inbound_arrival_time": Offer.inbound_arrival_datetime,
            "inbound_departure_airport": Offer.inbound_departure_airport,
            "inbound_departure_time": Offer.inbound_departure_datetime,
            "latest_return": Offer.outbound_departure_datetime,
            "mealtype": Offer.mealtype,
            "oceanview": Offer.oceanview,
            "outbound_arrival_airport": Offer.outbound_arrival_airport,
            "outbound_arrival_time": Offer.outbound_arrival_datetime,
            "outbound_departure_time": Offer.outbound_departure_datetime,
            "price_max": Offer.price,
            "price_min": Offer.price,
            "roomtype": Offer.roomtype
        }
        self._parameter_filter_mapping = {
            "adults": self._generic_equals_filter,
            "children": self._generic_equals_filter,
            "duration": self._generic_equals_filter,
            "earliest_departure": partial(self._date_comparison_filter, op=operator.ge),
            "inbound_arrival_time": self._time_filter,
            "inbound_departure_airport": self._generic_equals_filter,
            "inbound_departure_time": self._time_filter,
            "latest_return": partial(self._date_comparison_filter, op=operator.le),
            "mealtype": self._generic_equals_filter,
            "oceanview": self._generic_equals_filter,
            "outbound_arrival_time": self._time_filter,
            "outbound_arrival_airport": self._generic_equals_filter,
            "outbound_departure_time": self._time_filter,
            "price_max": partial(self._generic_comparison_filter, op=operator.le),
            "price_min": partial(self._generic_comparison_filter, op=operator.ge),
            "roomtype": self._generic_equals_filter
        }

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

    def _filter_all_offers(self) -> Subquery:
        """ Applies all filters to the Offer table based on the query parameters the user provided.

        Returns
        -------
        Subquery
            A subquery containing all offers that match the given query parameters.
        """

        non_null_params = self._extract_non_null_query_params()
        query = select(Offer)
        for param in non_null_params:
            attribute = self._schema_attribute_mapping[param]
            query = self._parameter_filter_mapping[param](attribute=attribute, query=query, value=non_null_params[param])

        return query.subquery("filtered_offers")

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

    def _get_cheapest_offers(self, query: Subquery) -> Subquery:
        """ Returns a subquery that contains the cheapest offer per hotel from the given query.

        Parameters
        ----------
        query : Subquery
            A subquery containing the offers to be filtered.

        Returns
        -------
        Subquery
            A subquery containing the cheapest offer per hotel.
        """

        cheapest_offers_query = select(
            query.columns.hotel_id,
            func.min(query.columns.price).label("min_price"),
            func.min(query.columns.offer_id).label("min_offer_id"),
            func.count(query.columns.hotel_id).label("count_offers")
        ).group_by(
            query.columns.hotel_id
        ).subquery("cheapest_offers")

        return cheapest_offers_query

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

        filtered_offers_subquery = self._filter_all_offers()
        cheapest_offers_subquery = self._get_cheapest_offers(query=filtered_offers_subquery)
        final_query = select(
            Hotel.hotel_name,
            Hotel.hotel_stars,
            Offer.mealtype,
            Offer.roomtype,
            Offer.offer_id,
            Offer.count_adults,
            Offer.count_children,
            Offer.price,
            Offer.duration,
            cheapest_offers_subquery.columns.count_offers,
        ).join(
            target=Hotel,
            onclause=Offer.hotel_id==Hotel.hotel_id
        ).join(
            target=cheapest_offers_subquery,
            onclause=(Offer.offer_id == cheapest_offers_subquery.columns.min_offer_id)
        )

        return final_query
