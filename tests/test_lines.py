import pytest

from mobtapi.transport.lines import (
    Line,
    _parse_line,
    _parse_lines,
    get_lines,
    get_line,
)


@pytest.fixture
def line_data():
    return {
        "id": "11:1",
        "shortName": "C1",
        "longName": "CIRCULAR CENTRO",
        "color": "ED4713",
        "textColor": "000000",
        "agencyId": "11",
        "timeZone": "Europe/Madrid",
        "companyZoneId": 11,
    }


@pytest.fixture
def line_detail_data():
    return {
        "id": "11:1",
        "shortName": "C1",
        "longName": "CIRCULAR CENTRO",
        "color": "ED4713",
        "textColor": "000000",
        "bikesAllowed": 0,
        "type": 3,
        "agencyId": "11",
        "timeZone": "Europe/Madrid",
        "companyZoneId": 11,
    }


def test_parse_line(line_data):
    line = _parse_line(line_data)

    assert isinstance(line, Line)
    assert line.id == "11:1"
    assert line.short_name == "C1"
    assert line.long_name == "CIRCULAR CENTRO"
    assert line.color == "ED4713"
    assert line.text_color == "000000"
    assert line.agency_id == "11"
    assert line.time_zone == "Europe/Madrid"
    assert line.company_zone_id == 11


def test_parse_line_optional_fields(line_data):
    line = _parse_line(line_data)

    assert line.bikes_allowed is None
    assert line.type is None


def test_parse_line_detail(line_detail_data):
    line = _parse_line(line_detail_data)

    assert line.bikes_allowed == 0
    assert line.type == 3


def test_parse_lines(line_data):
    lines = _parse_lines([line_data, line_data])

    assert len(lines) == 2
    assert all(isinstance(line, Line) for line in lines)
    assert lines[0].short_name == "C1"


def test_line_repr(line_data):
    line = _parse_line(line_data)

    assert repr(line) == "C1"


def test_get_lines(monkeypatch, line_data):
    def mock_get(endpoint):
        assert endpoint == "routers/galicia/index/routes"
        return [line_data]

    monkeypatch.setattr(
        "mobtapi.transport.lines._api_client.get",
        mock_get,
    )

    lines = get_lines()

    assert len(lines) == 1
    assert isinstance(lines[0], Line)
    assert lines[0].id == "11:1"


def test_get_line(monkeypatch, line_detail_data):
    def mock_get(endpoint):
        assert endpoint == "routers/galicia/index/routes/11:1"
        return line_detail_data

    monkeypatch.setattr(
        "mobtapi.transport.lines._api_client.get",
        mock_get,
    )

    line = get_line("11:1")

    assert isinstance(line, Line)
    assert line.id == "11:1"
    assert line.short_name == "C1"
    assert line.bikes_allowed == 0
    assert line.type == 3