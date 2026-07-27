import requests
from json import JSONDecodeError


class APIClient():
    """Client to interact with the Arriva API."""

    def __init__(self, api_url):
        self.api_url = api_url
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0.0.0 Safari/537.36"
            )
        }

    def _request(self, method, endpoint):
        """Make a HTTP request to the API."""
        url = self.api_url + endpoint
        try:
            response = requests.request(method=method, url=url)
        except requests.RequestException as e:
            raise e
        
        try:
            return response.json()
        except (ValueError, JSONDecodeError) as e:
            raise e

    def get(self, endpoint):
        """Make a GET request to the API."""
        return self._request("GET", endpoint)