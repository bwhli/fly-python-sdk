from typing import Optional

import httpx

from fly_python_sdk import (
    DEFAULT_API_TIMEOUT,
    FLY_MACHINES_API_DEFAULT_API_HOSTNAME,
    FLY_MACHINES_API_VERSION,
)
from fly_python_sdk.models import FlyApp, FlyAppCreateRequest, FlyMachine


class Fly:
    def __init__(
        self,
        api_token,
        api_timeout=DEFAULT_API_TIMEOUT,
        api_version=FLY_MACHINES_API_VERSION,
        base_url=FLY_MACHINES_API_DEFAULT_API_HOSTNAME,
    ):
        self.api_token = api_token
        self.api_timeout = api_timeout
        self.api_version = api_version
        self.base_url = base_url

    def Org(
        self,
        org_slug: str = "personal",
    ):
        return Org(
            self,
            org_slug,
        )

    async def _make_api_delete_request(
        self,
        url_path: str,
    ) -> httpx.Response:
        """An internal function for making DELETE requests to the Fly API."""
        url = f"{self.base_url}/v{self.api_version}/{url_path}"
        async with httpx.AsyncClient(timeout=self.api_timeout) as client:
            r = await client.delete(
                url,
                headers=self._generate_headers(),
            )
        return r

    async def _make_api_get_request(
        self,
        url_path: str,
    ) -> httpx.Response:
        """An internal function for making GET requests to the Fly API."""
        url = f"{self.base_url}/v{self.api_version}/{url_path}"
        async with httpx.AsyncClient(timeout=self.api_timeout) as client:
            r = await client.get(
                url,
                headers=self._generate_headers(),
            )
        return r

    async def _make_api_post_request(
        self,
        url_path: str,
        payload: dict = {},
    ) -> httpx.Response:
        """An internal function for making POST requests to the Fly API."""
        url = f"{self.base_url}/v{self.api_version}/{url_path}"
        async with httpx.AsyncClient(timeout=self.api_timeout) as client:
            r = await client.post(
                url,
                headers=self._generate_headers(),
                json=payload,
            )
        return r

    def _generate_headers(
        self,
    ) -> dict:
        """Returns a dictionary containing headers for requests to the Fly API."""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        return headers


class Org(Fly):
    def __init__(
        self,
        fly: Fly,
        org_slug,
    ):
        super().__init__(
            fly.api_token,
            fly.api_timeout,
            fly.api_version,
            fly.base_url,
        )
        self.org_slug = org_slug

    def App(
        self,
        app_name,
    ):
        return App(
            self,
            app_name,
        )


class App(Fly):
    def __init__(
        self,
        org: Org,
        app_name: str,
    ):
        super().__init__(
            org.api_token,
            org.api_timeout,
            org.api_version,
            org.base_url,
        )
        self.app_name = app_name
        self.org_slug = org.org_slug

    async def create(
        self,
        network: str = "default",
        org_slug: str = "personal",
    ):
        """Creates a new app on Fly.

        Args:
            app_name: The name of the new Fly app.
            org_slug: The slug of the organization to create the app within.
        """
        app_details = FlyAppCreateRequest(
            app_name=self.app_name,
            network=network,
            org_slug=org_slug,
        )

        r = await self._make_api_post_request(
            "apps",
            app_details.model_dump(),
        )

        if r.status_code != 201:
            raise Exception(message=f"Unable to create {self.app_name} in {org_slug}.")

        return

    async def delete(self):
        """
        Deletes a Fly app.
        """
        r = await self._make_api_delete_request(f"apps/{self.app_name}")

        if r.status_code != 202:
            raise Exception(message=f"Could not delete {self.app_name}.")

        return

    async def list_machines(
        self,
        regions: list[str] = [],
        ids_only: bool = False,
    ) -> list[FlyMachine] | list[str]:
        """Returns a list of machines that belong to a Fly application.

        Args:
            ids_only: If True, only machine IDs will be returned. Defaults to False.
        """
        url_path = f"apps/{self.app_name}/machines"
        r = await self._make_api_get_request(url_path)

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise Exception(message=f"Unable to get machines in {self.app_name}!")

        # Create a FlyMachine object for each machine.
        machines = [FlyMachine(**machine) for machine in r.json()]

        # Filter regions as needed.
        if len(regions) > 0:
            machines = [machine for machine in machines if machine.region in regions]

        # Filter and return a list of ids if ids_only is True.
        if ids_only is True:
            return [machine.id for machine in machines]

        return machines

    async def inspect(self):
        """
        Fetches the details of a Fly app.
        """
        r = await self._make_api_get_request(f"apps/{self.app_name}")

        if r.status_code != 200:
            raise Exception(message=f"Could not find {self.app_name}.")

        return FlyApp(**r.json())

    def Machine(
        self,
        machine_id: str,
    ):
        return Machine(
            self,
            machine_id,
        )


class Machine(Fly):
    def __init__(
        self,
        app: App,
        machine_id: Optional[str] = None,
    ):
        super().__init__(
            app.api_token,
            app.api_timeout,
            app.api_version,
            app.base_url,
        )
        self.app_name = app.app_name
        self.org_slug = app.org_slug
        self.machine_id = machine_id

    async def inspect(
        self,
    ) -> FlyMachine:
        """Returns information about a Fly machine.

        Args:
            app_name: The name of the new Fly app.
            machine_id: The id string for a Fly machine.
        """
        if not self.machine_id:
            raise Exception(
                message="Please provide the ID of the Machine you want to inspect."
            )

        r = await self._make_api_get_request(
            f"apps/{self.app_name}/machines/{self.machine_id}"
        )

        if r.status_code != 200:
            raise Exception(
                message=f"Unable to delete {self.machine_id} in {self.app_name}!"
            )

        return FlyMachine(**r.json())
