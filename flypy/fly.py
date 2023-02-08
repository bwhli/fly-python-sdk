import os

import requests
from exceptions import MissingApiHostnameError, MissingApiTokenError
from models import FlyAppDetailsResponse, FlyMachineDetailsResponse
from requests import Response


class Fly:
    def __init__(self, app_name: str) -> None:
        self.app_name = app_name
        self.api_hostname = self._get_api_hostname()
        self.api_token = self._get_api_token()
        self.api_version = 1

    def get_app(self) -> FlyAppDetailsResponse:
        """
        Returns information about a Fly.io application.
        """
        path = f"apps/{self.app_name}"
        r = self._make_api_get_request(path)
        return FlyAppDetailsResponse(**r.json())

    def get_machine(self, machine_id: str) -> FlyMachineDetailsResponse:
        """Returns information about a Fly.io machine.

        Args:
            machine_id: The id string for a Fly.io machine.
        """
        path = f"apps/{self.app_name}/machines/{machine_id}"
        r = self._make_api_get_request(path)
        return FlyMachineDetailsResponse(**r.json())

    def get_machines(self, ids_only: bool = False) -> list[FlyMachineDetailsResponse]:
        """Returns a list of machines that belong to a Fly.io application.

        Args:
            ids_only: If True, only machine IDs will be returned. Defaults to False.
        """
        path = f"apps/{self.app_name}/machines"
        r = self._make_api_get_request(path)
        machines = [FlyMachineDetailsResponse(**machine) for machine in r.json()]
        # Filter and return a list of ids if ids_only is True.
        if ids_only is True:
            return [machine.id for machine in machines]
        return machines

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
        """
        Returns the hostname that will be used to connect to the Fly.io API.

        Returns:
            The hostname that will be used to connect to the Fly.io API.

        Raises:
            MissingApiHostnameError: If FLY_API_HOSTNAME is not set as an environment variable.
        """
        try:
            api_hostname = os.environ["FLY_API_HOSTNAME"]
            return api_hostname
        except KeyError:
            raise MissingApiHostnameError(
                "Please configure the FLY_API_HOSTNAME environment variable."
            )

    def _get_api_token(self) -> str:
        """
        Returns the API token that will be used to connect to the Fly.io API.

        Returns:
            The API token that will be used to connect to the Fly.io API.

        Raises:
            MissingApiTokenError: If FLY_API_TOKEN is not set as an environment variable.
        """
        try:
            api_token = os.environ["FLY_API_TOKEN"]
            return api_token
        except KeyError:
            raise MissingApiTokenError(
                "Please configure the FLY_API_TOKEN environment variable."
            )
