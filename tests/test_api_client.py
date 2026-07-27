import pytest
import requests

from mobtapi.api_client import APIClient


def test_api_client_initialization():
    client = APIClient("https://api.example.com/")

    assert client.api_url == "https://api.example.com/"
    assert "User-Agent" in client.headers


def test_get_request(monkeypatch):
    client = APIClient("https://api.example.com/")

    class MockResponse:
        def json(self):
            return {"status": "ok"}

    def mock_request(method, url):
        assert method == "GET"
        assert url == "https://api.example.com/test"

        return MockResponse()

    monkeypatch.setattr(requests, "request", mock_request)

    response = client.get("test")

    assert response == {"status": "ok"}


def test_request_exception(monkeypatch):
    client = APIClient("https://api.example.com/")

    def mock_request(method, url):
        raise requests.RequestException("Connection error")

    monkeypatch.setattr(requests, "request", mock_request)

    with pytest.raises(requests.RequestException):
        client.get("test")


def test_invalid_json_response(monkeypatch):
    client = APIClient("https://api.example.com/")

    class MockResponse:
        def json(self):
            raise ValueError("Invalid JSON")

    def mock_request(method, url):
        return MockResponse()

    monkeypatch.setattr(requests, "request", mock_request)

    with pytest.raises(ValueError):
        client.get("test")