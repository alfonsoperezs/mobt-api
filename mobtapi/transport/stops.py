from . import _api_client


class Stop:
    """A public transport stop."""

    def __init__(
        self,
        id,
        code=None,
        name=None,
        lat=None,
        lon=None,
        routes=None,
        airport=None,
        company_zone_id=None,
        location_type=None,
        scheduled_arrival=None,
        time_zone=None,
        virtual_level=None,
        wheelchair_boarding=None,
        x=None,
        y=None,
        zone_id=None,
    ):
        self.id = id
        """Unique identifier of the stop."""

        self.code = code
        """Public code of the stop."""

        self.name = name
        """Name of the stop."""

        self.lat = lat
        """Latitude of the stop."""

        self.lon = lon
        """Longitude of the stop."""

        self.routes = routes
        """Routes serving the stop."""

        self.airport = airport
        """Whether the stop is located at an airport."""

        self.company_zone_id = company_zone_id
        """Identifier of the company zone."""

        self.location_type = location_type
        """GTFS location type."""

        self.scheduled_arrival = scheduled_arrival
        """Scheduled arrival time."""

        self.time_zone = time_zone
        """Time zone of the stop."""

        self.virtual_level = virtual_level
        """Virtual level of the stop."""

        self.wheelchair_boarding = wheelchair_boarding
        """Wheelchair accessibility information."""

        self.x = x
        """X coordinate of the stop."""

        self.y = y
        """Y coordinate of the stop."""

        self.zone_id = zone_id
        """Fare zone identifier."""

    def __repr__(self):
        return str(self.name)


def _parse_stop(data: dict) -> Stop:
    """
    Parse a stop from API response data.

    Args:
        data (dict): Stop data returned by the API.

    Returns:
        Stop: Parsed stop object.
    """
    return Stop(
        id=data.get("id"),
        code=data.get("code"),
        name=data.get("name"),
        lat=data.get("lat"),
        lon=data.get("lon"),
        routes=data.get("routes"),
        airport=data.get("airport"),
        company_zone_id=data.get("companyZoneId"),
        location_type=data.get("locationType"),
        scheduled_arrival=data.get("scheduledArrival"),
        time_zone=data.get("timeZone"),
        virtual_level=data.get("virtualLevel"),
        wheelchair_boarding=data.get("wheelchairBoarding"),
        x=data.get("x"),
        y=data.get("y"),
        zone_id=data.get("zoneId"),
    )


def _parse_stops(data: list[dict]) -> list[Stop]:
    """
    Parse a list of stops from API response data.

    Args:
        data (list[dict]): List of stop dictionaries.

    Returns:
        list[Stop]: Parsed stops.
    """
    return [_parse_stop(stop) for stop in data]


def get_stops() -> list[Stop]:
    """
    Get all available stops from the MOBT API.

    Returns:
        list[Stop]: List of available public transport stops.

    Raises:
        requests.RequestException: If the API request fails.
        ValueError: If the API response cannot be decoded as JSON.
    """
    return _parse_stops(
        _api_client.get("routers/galicia/index/stops")
    )


def get_trip_stops(trip_id: str) -> list[Stop]:
    """
    Get the stops of a trip.

    Args:
        trip_id (str): Identifier of the trip.

    Returns:
        list[Stop]: List of stops belonging to the trip.

    Raises:
        requests.RequestException: If the API request fails.
        ValueError: If the API response cannot be decoded as JSON.
    """
    endpoint = f"routers/galicia/index/trips/{trip_id}/stops"
    return _parse_stops(_api_client.get(endpoint))