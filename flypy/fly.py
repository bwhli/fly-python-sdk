import os

import requests
from models import FlyAppDetails
from requests import Response


class Fly:
    def __init__(self, app_name: str) -> None:
        self.app_name = app_name
        self.api_hostname = self._get_api_hostname()
        self.api_token = self._get_api_token()
        self.api_version = 1

    def get_app_details(self) -> FlyAppDetails:
        """
        Returns information about a Fly.io application.
        """
        path = f"apps/{self.app_name}"
        r = self._make_api_get_request(path)
        return FlyAppDetails(**r.json())

    def _make_api_get_request(self, path: str) -> Response:
        url = f"http://{self.api_hostname}/v{self.api_version}/{path}"
        r = requests.get(url, headers=self._generate_headers())
        r.raise_for_status()
        return r

    def _make_api_post_request() -> Response:
        return

    #############
    # Utilities #
    #############

    def _generate_headers(self) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        return headers

    def _get_api_hostname(self) -> str:
        api_hostname = os.environ["FLY_API_HOSTNAME"]
        return api_hostname

    def _get_api_token(self) -> str:
        api_token = os.environ["FLY_API_TOKEN"]
        return api_token
