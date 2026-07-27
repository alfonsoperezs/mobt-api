import pytest

from mobtapi.transport.stops import (
    Stop,
    _parse_stop,
    _parse_stops,
    get_stops,
    get_trip_stops,
)


@pytest.fixture
def stop_data():
    return {
        "airport": False,
        "code": "574",
        "companyZoneId": 3,
        "id": "3:574",
        "lat": 43.344278,
        "locationType": 0,
        "lon": -8.450893,
        "name": "Meicende, Av. Butano",
        "scheduledArrival": 0,
        "timeZone": "Europe/Madrid",
        "virtualLevel": 0,
        "wheelchairBoarding": 0,
        "x": -8.450893,
        "y": 43.344278,
    }


def test_parse_stop(stop_data):
    stop = _parse_stop(stop_data)

    assert isinstance(stop, Stop)
    assert stop.id == "3:574"
    assert stop.code == "574"
    assert stop.name == "Meicende, Av. Butano"
    assert stop.lat == 43.344278
    assert stop.lon == -8.450893
    assert stop.company_zone_id == 3
    assert stop.time_zone == "Europe/Madrid"


def test_parse_stop_optional_fields(stop_data):
    stop = _parse_stop(stop_data)

    assert stop.routes is None
    assert stop.zone_id is None


def test_parse_stops(stop_data):
    stops = _parse_stops([stop_data, stop_data])

    assert len(stops) == 2
    assert all(isinstance(stop, Stop) for stop in stops)
    assert stops[0].name == "Meicende, Av. Butano"


def test_stop_repr(stop_data):
    stop = _parse_stop(stop_data)

    assert repr(stop) == "Meicende, Av. Butano"


def test_get_stops(monkeypatch, stop_data):
    def mock_get(endpoint):
        assert endpoint == "routers/galicia/index/stops"
        return [stop_data]

    monkeypatch.setattr(
        "mobtapi.transport.stops._api_client.get",
        mock_get,
    )

    stops = get_stops()

    assert len(stops) == 1
    assert isinstance(stops[0], Stop)
    assert stops[0].id == "3:574"


def test_get_trip_stops(monkeypatch, stop_data):
    def mock_get(endpoint):
        assert endpoint == "routers/galicia/index/trips/3:603070700/stops"
        return [stop_data]

    monkeypatch.setattr(
        "mobtapi.transport.stops._api_client.get",
        mock_get,
    )

    stops = get_trip_stops("3:603070700")

    assert len(stops) == 1
    assert isinstance(stops[0], Stop)
    assert stops[0].name == "Meicende, Av. Butano"


def test_get_trip_stops_with_missing_fields(monkeypatch):
    data = [
        {
            "id": "3:574",
            "name": "Meicende, Av. Butano",
            "lat": 43.344278,
            "lon": -8.450893,
        }
    ]

    monkeypatch.setattr(
        "mobtapi.transport.stops._api_client.get",
        lambda endpoint: data,
    )

    stops = get_trip_stops("3:603070700")

    assert len(stops) == 1
    assert stops[0].routes is None
    assert stops[0].zone_id is None