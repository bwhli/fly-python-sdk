import logging
from typing import Optional

import httpx

from fly_python_sdk import (
    DEFAULT_API_TIMEOUT,
    FLY_MACHINE_DEFAULT_WAIT_TIMEOUT,
    FLY_MACHINE_STATES,
    FLY_MACHINES_API_DEFAULT_API_HOSTNAME,
    FLY_MACHINES_API_VERSION,
)
from fly_python_sdk.models import (
    FlyApp,
    FlyAppCreateRequest,
    FlyApps,
    FlyMachine,
    FlyMachineConfig,
)


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
        async with httpx.AsyncClient(
            timeout=self.api_timeout,
        ) as client:
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
        async with httpx.AsyncClient(
            timeout=self.api_timeout,
        ) as client:
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
        async with httpx.AsyncClient(
            timeout=self.api_timeout,
        ) as client:
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

    async def list_apps(
        self,
        sort_by: str = "name",
    ):
        """
        Returns a list of apps that belong to a Fly organization.

        Args:
            org_slug (str): The slug of the organization to create the app within.
            sort_by (str): The field to sort the list of apps by.
                Valid values are "machine_count", "name", and "network".
                Defaults to "name".
        """
        if sort_by not in ["machine_count", "name", "network"]:
            raise Exception(
                "Invalid sort_by value. Valid sort_by values are 'machine_count', 'name', and 'network'."
            )

        r = await self._make_api_get_request(f"apps?org_slug={self.org_slug}")

        if r.status_code != 200:
            raise Exception(
                message=f"Could not find apps in the {self.org_slug} organization."
            )

        apps = FlyApps(**r.json())
        apps.apps = sorted(
            apps.apps,
            key=lambda app: getattr(
                app,
                sort_by,
            ),
        )

        return apps


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

    def Machine(
        self,
        machine_id: str,
    ):
        return Machine(
            self,
            machine_id,
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

    async def create(
        self,
        config: FlyMachineConfig,
        name: str = None,
        region: str = None,
        wait_for_started_state: bool = True,
    ) -> FlyMachine:
        """Creates a Fly machine.

        Args:
            app_name: The name of the new Fly app.
            config: A FlyMachineConfig object containing creation details.
            name: The name of the machine.
            region: The deployment region for the machine.
        """
        if self.machine_id:
            raise Exception(
                message="Machine IDs are assigned by Fly after creation. Please do not provide a machine ID when creating a new machine."
            )

        # Create Pydantic model for machine creation requests.
        machine = FlyMachine(
            name=name,
            region=region,
            config=config,
        )

        r = await self._make_api_post_request(
            f"apps/{self.app_name}/machines",
            payload=machine.model_dump(exclude_none=True),
        )

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise Exception(message=f"{r.status_code}: Unable to create machine!")

        created_machine = FlyMachine(**r.json())

        # Newly created Machines should start automatically,
        # so wait for the created machine to enter the "started" state.
        if wait_for_started_state is True:
            await self.wait_machine(
                self.app_name,
                created_machine.id,
                "started",
            )

        logging.info(f"Machine {created_machine.id} has been created in {region}.")

        return created_machine

    async def destroy_machine(
        self,
        wait_for_detroyed_state: bool = True,
    ) -> None:
        """Destroys a Fly machine.

        Args:
            app_name: The name of the new Fly app.
            machine_id: The id string for a Fly machine.
        """
        if not self.machine_id:
            raise Exception(message="Please provide the ID of the Machine to destroy.")
        # Fetch the Machine object.
        machine = await self.get_machine(
            self.app_name,
            self.machine_id,
        )

        # Stop the machine if it is not already stopped.
        if machine.state != "stopped":
            await self.stop_machine(
                self.app_name,
                self.machine_id,
            )

        r = await self._make_api_delete_request(
            f"apps/{self.app_name}/machines/{self.machine_id}"
        )

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise Exception(
                message=f"Unable to delete {self.machine_id} in {self.app_name}!"
            )

        logging.info(f"Machine {self.machine_id} has been deleted.")

        # Wait for the machine to enter the "destroyed" state.
        if wait_for_detroyed_state is True:
            await self.wait_machine(
                self.app_name,
                self.machine_id,
                "destroyed",
            )

        return

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

    async def start_machine(
        self,
        wait_for_started_state: bool = True,
    ) -> None:
        """Starts a Fly machine.

        Args:
            app_name: The name of the new Fly app.
            machine_id: The id string for a Fly machine.
        """
        r = await self._make_api_post_request(
            f"apps/{self.app_name}/machines/{self.machine_id}/start"
        )

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise Exception(
                message=f"Unable to start {self.machine_id} in {self.app_name}!"
            )

        if wait_for_started_state is True:
            await self.wait_machine(self.app_name, self.machine_id, "started")

        return

    async def stop_machine(
        self,
    ) -> None:
        """Stop a Fly machine.

        Args:
            app_name: The name of the new Fly app.
            machine_id: The id string for a Fly machine.
        """
        # Wait for the machine to reach "started" state before trying to stop it.
        # await self.wait_machine(app_name, machine_id, "started")

        # machine = await self.get_machine(self.app_name, self.machine_id)

        machine = await self.get_machine(self.app_name, self.machine_id)

        # Return if the machine is already stopped.
        if machine.state == "stopped":
            return

        logging.info(f"Attemping to stop {self.machine_id} in {self.app_name}.")

        r = await self._make_api_post_request(
            f"apps/{self.app_name}/machines/{self.machine_id}/stop"
        )

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise Exception(
                message=f"Unable to stop {self.machine_id} in {self.app_name}!"
            )

        logging.info(f"Stopped {self.machine_id} in {self.app_name}.")

        await self.wait_machine(self.app_name, self.machine_id, "stopped")

        return

    async def wait_machine(
        self,
        target_state: str,
        timeout: int = FLY_MACHINE_DEFAULT_WAIT_TIMEOUT,
    ) -> None:
        """Waits for a Fly machine to be reach the target state.

        Args:
            app_name: The name of the new Fly app.
            machine_id: The id string for a Fly machine.
            instance_id: The id string for a Fly instance.
            target_state: The target state for the machine.
            timeout: The maximum time to wait for the machine to reach the target state.
        """

        if target_state not in FLY_MACHINE_STATES:
            raise Exception(message=f'"{target_state}" is not a valid machine state.')

        # Fetch the Machine object to get the instance ID.
        machine = await self.get_machine(self.app_name, self.machine_id)

        logging.info(
            f'Waiting for {self.machine_id} in {self.app_name} to reach "{target_state}" state.'
        )

        r = await self._make_api_get_request(
            f"apps/{self.app_name}/machines/{self.machine_id}/wait?instance_id={machine.instance_id}&state={target_state}&timeout={timeout}"
        )

        if r.status_code != 200:
            raise Exception(
                message=f'{self.machine_id} in {self.app_name} was unable to to reach "{target_state}" state.'
            )

        logging.info(f'Machine {self.machine_id} has reached "{target_state}" state.')

        return
