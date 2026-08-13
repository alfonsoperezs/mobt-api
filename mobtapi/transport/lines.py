from . import _api_client

class Line:
    """A public transport line."""

    def __init__(
        self,
        id,
        short_name,
        long_name,
        color,
        text_color,
        bikes_allowed=None,
        type=None,
        agency_id=None,
        time_zone=None,
        company_zone_id=None,
    ):
        self.id = id
        """Unique identifier of the line."""

        self.short_name = short_name
        """Short name or code of the line."""

        self.long_name = long_name
        """Full name or description of the line."""

        self.color = color
        """Color used to represent the line."""

        self.text_color = text_color
        """Text color used when displaying the line."""

        self.bikes_allowed = bikes_allowed
        """Whether bicycles are allowed on the line."""

        self.type = type
        """GTFS route type of the line."""

        self.agency_id = agency_id
        """Identifier of the agency operating the line."""

        self.time_zone = time_zone
        """Time zone of the line."""

        self.company_zone_id = company_zone_id
        """Identifier of the company zone."""

    def __repr__(self):
        return str(self.short_name)


def _parse_line(data: dict) -> Line:
    """
    Parse a line from API response data.

    Args:
        data (dict): Line data returned by the API.

    Returns:
        Line: Parsed line object.
    """
    return Line(
        id=data.get("id"),
        short_name=data.get("shortName"),
        long_name=data.get("longName"),
        color=data.get("color"),
        text_color=data.get("textColor"),
        bikes_allowed=data.get("bikesAllowed"),
        type=data.get("type"),
        agency_id=data.get("agencyId"),
        time_zone=data.get("timeZone"),
        company_zone_id=data.get("companyZoneId"),
    )


def _parse_lines(data: list[dict]) -> list[Line]:
    """
    Parse a list of lines from API response data.

    Args:
        data (list[dict]): List of line dictionaries.

    Returns:
        list[Line]: Parsed lines.
    """
    return [_parse_line(line) for line in data]


def get_lines() -> list[Line]:
    """
    Get all available public transport lines from the MOBT API.

    Returns:
        list[Line]: List of available public transport lines.

    Raises:
        requests.RequestException: If the API request fails.
        ValueError: If the API response cannot be decoded as JSON.
    """
    return _parse_lines(
        _api_client.get("routers/galicia/index/routes")
    )


def get_line(line_id: str) -> Line:
    """
    Get the details of a public transport line.

    Args:
        line_id (str): Identifier of the line.

    Returns:
        Line: Line details.

    Raises:
        requests.RequestException: If the API request fails.
        ValueError: If the API response cannot be decoded as JSON.
    """
    return _parse_line(_api_client.get(f"routers/galicia/index/routes/{line_id}"))