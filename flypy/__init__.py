import os

import requests

from flypy.models import FlyAppDetailsResponse, FlyMachineDetailsResponse


class FlyClient:
    def __init__(self, api_token: str, app_name: str) -> None:
        self.app_name = app_name
        self.api_token = api_token
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

    def _make_api_get_request(self, path: str) -> requests.Response:
        api_hostname = self._get_api_hostname()
        url = f"{api_hostname}/v{self.api_version}/{path}"
        r = requests.get(url, headers=self._generate_headers())
        r.raise_for_status()
        return r

    def _make_api_post_request() -> requests.Response:
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
            If the FLY_API_HOSTNAME environment variable is not set,
            the hostname returned will default to https://api.machines.dev.
        """
        api_hostname = os.getenv("FLY_API_HOSTNAME", "https://api.machines.dev")
        return api_hostname
