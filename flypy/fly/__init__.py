import os

import requests

from flypy.models.apps import FlyAppCreateRequest, FlyAppDetailsResponse
from flypy.models.machines import FlyMachineDetailsResponse


class Fly:
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token
        self.api_version = 1

    def _make_api_delete_request(
        self,
        path: str,
    ) -> requests.Response:
        """An internal function for making DELETE requests to the Fly.io API."""
        api_hostname = self._get_api_hostname()
        url = f"{api_hostname}/v{self.api_version}/{path}"
        r = requests.delete(url, headers=self._generate_headers())
        return r

    def _make_api_get_request(
        self,
        path: str,
    ) -> requests.Response:
        """An internal function for making GET requests to the Fly.io API."""
        api_hostname = self._get_api_hostname()
        url = f"{api_hostname}/v{self.api_version}/{path}"
        r = requests.get(url, headers=self._generate_headers())
        return r

    def _make_api_post_request(
        self,
        path: str,
        payload: dict,
    ) -> requests.Response:
        """An internal function for making POST requests to the Fly.io API."""
        api_hostname = self._get_api_hostname()
        url = f"{api_hostname}/v{self.api_version}/{path}"
        r = requests.post(url, headers=self._generate_headers(), json=payload)
        return r

    #############
    # Utilities #
    #############

    def _generate_headers(self) -> dict:
        """Returns a dictionary containing headers for requests to the Fly.io API."""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        return headers

    def _get_api_hostname(self) -> str:
        """Returns the hostname that will be used to connect to the Fly.io API.

        Returns:
            The hostname that will be used to connect to the Fly.io API.
            If the FLY_API_HOSTNAME environment variable is not set,
            the hostname returned will default to https://api.machines.dev.
        """
        api_hostname = os.getenv("FLY_API_HOSTNAME", "https://api.machines.dev")
        return api_hostname
