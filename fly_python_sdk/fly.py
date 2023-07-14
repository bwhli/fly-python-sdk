import asyncio
import logging
import os

import httpx
from rich import print

from fly_python_sdk import (
    DEFAULT_API_TIMEOUT,
    FLY_MACHINE_DEFAULT_WAIT_TIMEOUT,
    FLY_MACHINE_STATES,
    FLY_MACHINES_API_DEFAULT_API_HOSTNAME,
    FLY_MACHINES_API_VERSION,
)
from fly_python_sdk.exceptions import (
    AppInterfaceError,
    MachineInterfaceError,
    MachineInvalidStateError,
    MachineStateTransitionError,
    MissingApiTokenError,
    MissingMachineIdsError,
)
from fly_python_sdk.models import FlyAppCreateRequest, FlyMachine, FlyMachineConfig


class Fly:
    """Client for interacting with the Fly Machines API."""

    def __init__(
        self,
        api_token: str,
        base_url: str = FLY_MACHINES_API_DEFAULT_API_HOSTNAME,
        api_timeout: int = DEFAULT_API_TIMEOUT,
    ):
        """Initializes a new Fly client.

        Args:
            api_token: The Fly API token to use for authentication.
            base_url: The base URL of the Fly Machines API. Defaults to "https://api.machines.dev".
            api_timeout: The timeout for httx to use when making requests to the Fly Machines API. Default to 60s.
        """

        if api_token is None:
            raise MissingApiTokenError(
                message="Specify a valid Fly auth token for api_token, or set the FLY_API_TOKEN environment variable."
            )

        self.api_token = api_token
        self.api_version = FLY_MACHINES_API_VERSION
        self.base_url = base_url
        self.api_timeout = api_timeout

    ########
    # Apps #
    ########

    def create_app(
        self,
        app_name: str,
        org_slug: str,
    ) -> None:
        """Creates a new app on Fly.

        Args:
            app_name: The name of the new Fly app.
            org_slug: The slug of the organization to create the app within.
        """
        url_path = "apps"
        app_details = FlyAppCreateRequest(
            app_name=app_name,
            org_slug=org_slug,
        )
        r = self._make_api_post_request(url_path, app_details.model_dump())

        # Raise an exception if HTTP status code is not 201.
        if r.status_code != 201:
            raise AppInterfaceError(
                message=f"Unable to create {app_name} in {org_slug}!"
            )

        return FlyMachine(**r.json())

    ############
    # Machines #
    ############

    async def create_machine(
        self,
        app_name: str,
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
        # Create Pydantic model for machine creation requests.

        machine = FlyMachine(
            name=name,
            region=region,
            config=config,
        )

        r = await self._make_api_post_request(
            f"apps/{app_name}/machines",
            payload=machine.model_dump(exclude_none=True),
        )

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise MachineInterfaceError(
                message=f"{r.status_code}: Unable to create machine!"
            )

        created_machine = FlyMachine(**r.json())

        # Newly created Machines should start automatically,
        # so wait for the created machine to enter the "started" state.
        if wait_for_started_state is True:
            await self.wait_machine(app_name, created_machine.id, "started")

        logging.info(f"Machine {created_machine.id} has been created in {region}.")

        return created_machine

    async def destroy_machine(
        self,
        app_name: str,
        machine_id: str,
        wait_for_detroyed_state: bool = True,
    ) -> None:
        """Destroys a Fly machine.

        Args:
            app_name: The name of the new Fly app.
            machine_id: The id string for a Fly machine.
        """

        # Fetch the Machine object.
        machine = await self.get_machine(app_name, machine_id)

        # Stop the machine if it is not already stopped.
        if machine.state != "stopped":
            await self.stop_machine(app_name, machine_id)

        r = await self._make_api_delete_request(
            f"apps/{app_name}/machines/{machine_id}"
        )

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise MachineInterfaceError(
                message=f"Unable to delete {machine_id} in {app_name}!"
            )

        logging.info(f"Machine {machine_id} has been deleted.")

        # Wait for the machine to enter the "destroyed" state.
        if wait_for_detroyed_state is True:
            await self.wait_machine(app_name, machine_id, "destroyed")

        return

    async def destroy_machines(
        self,
        app_name: str,
        machine_ids: list[str] = [],
        destroy_all: bool = False,
    ) -> None:
        """Convenince function for destroying multiple Fly machines.

        Args:
            app_name: The name of the new Fly app.
            machine_ids: An array of machine IDs to delete.
            destroy_all: Delete all machines in the app if True.
        """
        # If delete_all is True, override provided machine_ids.
        if destroy_all is True:
            machine_ids = await self.list_machines(app_name, ids_only=True)
            logging.info(f"Machine IDs to delete: {', '.join(machine_ids)}.")

        # Raise an exception if there are no machine IDs to delete.
        if len(machine_ids) == 0:
            raise MissingMachineIdsError(
                "Please provide at least one machine ID to delete."
            )

        await asyncio.gather(
            *[self.destroy_machine(app_name, id) for id in machine_ids]
        )

        return

    async def get_machine(
        self,
        app_name: str,
        machine_id: str,
    ) -> FlyMachine:
        """Returns information about a Fly machine.

        Args:
            app_name: The name of the new Fly app.
            machine_id: The id string for a Fly machine.
        """
        url_path = f"apps/{app_name}/machines/{machine_id}"
        r = await self._make_api_get_request(url_path)

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise MachineInterfaceError(
                message=f"Unable to delete {machine_id} in {app_name}!"
            )

        return FlyMachine(**r.json())

    async def list_machines(
        self,
        app_name: str,
        ids_only: bool = False,
    ) -> list[FlyMachine] | list[str]:
        """Returns a list of machines that belong to a Fly application.

        Args:
            ids_only: If True, only machine IDs will be returned. Defaults to False.
        """
        url_path = f"apps/{app_name}/machines"
        r = await self._make_api_get_request(url_path)

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise AppInterfaceError(message=f"Unable to get machines in {app_name}!")

        print(r.json())

        # Create a FlyMachine object for each machine.
        machines = [FlyMachine(**machine) for machine in r.json()]

        # Filter and return a list of ids if ids_only is True.
        if ids_only is True:
            return [machine.id for machine in machines]

        return machines

    async def start_machine(
        self,
        app_name: str,
        machine_id: str,
        wait_for_started_state: bool = True,
    ) -> None:
        """Starts a Fly machine.

        Args:
            app_name: The name of the new Fly app.
            machine_id: The id string for a Fly machine.
        """
        r = await self._make_api_post_request(
            f"apps/{app_name}/machines/{machine_id}/start"
        )

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise MachineInterfaceError(
                message=f"Unable to start {machine_id} in {app_name}!"
            )

        if wait_for_started_state is True:
            await self.wait_machine(app_name, machine_id, "started")

        return

    async def stop_machine(
        self,
        app_name: str,
        machine_id: str,
    ) -> None:
        """Stop a Fly machine.

        Args:
            app_name: The name of the new Fly app.
            machine_id: The id string for a Fly machine.
        """
        # Wait for the machine to reach "started" state before trying to stop it.
        # await self.wait_machine(app_name, machine_id, "started")

        # machine = await self.get_machine(app_name, machine_id)

        machine = await self.get_machine(app_name, machine_id)

        # Return if the machine is already stopped.
        if machine.state == "stopped":
            return

        logging.info(f"Attemping to stop {machine_id} in {app_name}.")

        r = await self._make_api_post_request(
            f"apps/{app_name}/machines/{machine_id}/stop"
        )

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise MachineInterfaceError(
                message=f"Unable to stop {machine_id} in {app_name}!"
            )

        logging.info(f"Stopped {machine_id} in {app_name}.")

        await self.wait_machine(app_name, machine_id, "stopped")

        return

    async def wait_machine(
        self,
        app_name: str,
        machine_id: str,
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
            raise MachineInvalidStateError(
                message=f'"{target_state}" is not a valid machine state.'
            )

        # Fetch the Machine object to get the instance ID.
        machine = await self.get_machine(app_name, machine_id)

        logging.info(
            f'Waiting for {machine_id} in {app_name} to reach "{target_state}" state.'
        )

        r = await self._make_api_get_request(
            f"apps/{app_name}/machines/{machine_id}/wait?instance_id={machine.instance_id}&state={target_state}&timeout={timeout}"
        )

        if r.status_code != 200:
            raise MachineStateTransitionError(
                message=f'{machine_id} in {app_name} was unable to to reach "{target_state}" state.'
            )

        logging.info(f'Machine {machine_id} has reached "{target_state}" state.')

        return

    #####################
    # Utility Functions #
    #####################

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

    def _generate_headers(self) -> dict:
        """Returns a dictionary containing headers for requests to the Fly API."""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        return headers
