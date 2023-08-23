

from fly_python_sdk.fly.api import FlyApi
from fly_python_sdk.fly.machine import Machine
from fly_python_sdk.models import (
    FlyApp,
    FlyAppCreateRequest,
    FlyMachine,
)


class App(FlyApi):
    def __init__(
        self,
        api_token,
        org_slug,
        app_name,
    ):
        super().__init__(api_token)
        self.org_slug = org_slug
        self.app_name = app_name

    def Machine(
        self,
        machine_id: str,
    ) -> "Machine":
        return Machine(
            api_token=self.api_token,
            org_slug=self.org_slug,
            app_name=self.app_name,
            machine_id=machine_id,
        )

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

    async def delete(
        self,
    ):
        """
        Deletes a Fly app.
        """
        r = await self._make_api_delete_request(f"apps/{self.app_name}")

        if r.status_code != 202:
            raise Exception(message=f"Could not delete {self.app_name}.")

        return

    async def inspect(
        self,
    ):
        r = await self._make_api_get_request(f"apps/{self.app_name}")

        if r.status_code != 200:
            raise Exception(message=f"Could not find {self.app_name}.")

        return FlyApp(**r.json())

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
