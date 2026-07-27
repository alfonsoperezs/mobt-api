import pytest
from mobtapi.transport.stops import (
    Stop,
    _parse_stop,
    _parse_stops,
    get_stops,
)


@pytest.fixture
def stop_data():
    return {
        "airport": False,
        "code": "1038330",
        "companyZoneId": 37377,
        "id": "37377:03bf2182-35fd-43ba-839d-c5e3e02d06c3",
        "lat": 43.1165587,
        "locationType": 0,
        "lon": -8.0112272,
        "name": "ABELEDO",
        "routes": [],
        "scheduledArrival": 0,
        "timeZone": "Europe/Madrid",
        "virtualLevel": 0,
        "wheelchairBoarding": 2,
        "x": -8.0112272,
        "y": 43.1165587,
        "zoneId": "15032-3",
    }


def test_parse_stop(stop_data):
    stop = _parse_stop(stop_data)

    assert isinstance(stop, Stop)
    assert stop.id == "37377:03bf2182-35fd-43ba-839d-c5e3e02d06c3"
    assert stop.name == "ABELEDO"
    assert stop.lat == 43.1165587
    assert stop.lon == -8.0112272
    assert stop.company_zone_id == 37377
    assert stop.time_zone == "Europe/Madrid"


def test_parse_stops(stop_data):
    stops = _parse_stops([stop_data, stop_data])

    assert len(stops) == 2
    assert all(isinstance(stop, Stop) for stop in stops)
    assert stops[0].name == "ABELEDO"


def test_stop_repr(stop_data):
    stop = _parse_stop(stop_data)

    assert repr(stop) == "ABELEDO"


def test_get_stops(monkeypatch, stop_data):
    monkeypatch.setattr(
        "mobtapi.transport.stops._api_client.get",
        lambda endpoint: [stop_data],
    )

    stops = get_stops()

    assert len(stops) == 1
    assert isinstance(stops[0], Stop)
    assert stops[0].name == "ABELEDO"