import asyncio
import logging

from fly_python_sdk.exceptions import FlyError
from fly_python_sdk.fly.api import FlyApi
from fly_python_sdk.fly.machine import Machine
from fly_python_sdk.fly.volume import Volume
from fly_python_sdk.models.app import FlyApp
from fly_python_sdk.models.machine import FlyMachine, FlyMachineConfig


class App(FlyApi):
    """
    A class for interacting with Fly.io Apps.
    """

    def __init__(
        self,
        api_token,
        org_slug,
        app_name,
    ):
        super().__init__(api_token)
        self.org_slug = org_slug
        self.app_name = app_name

    ###################
    # App Methods #
    ###################

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

    ###################
    # Machine Methods #
    ###################

    async def create_machine(
        self,
        machine: FlyMachine,
    ) -> FlyMachine | str:
        """Creates a Fly machine.

        Args:
            app_name: The name of the new Fly app.
            config: A FlyMachineConfig object containing creation details.
            name: The name of the machine.
            region: The deployment region for the machine.
        """

        logging.info(f"Creating machine in this region: {machine.region}...")
        logging.info(f"Creating machine with this config: {machine.config}...")

        r = await self._make_api_post_request(
            f"apps/{self.app_name}/machines",
            payload=machine.model_dump(exclude_none=True),
        )

        if r.status_code != 200:
            logging.error(r.status_code)
            raise FlyError(message=f"{r.status_code}: Unable to create machine!")

        created_machine = FlyMachine(**r.json())

        logging.info(
            f"Machine {created_machine.id} has been created in {machine.region}."
        )

        return created_machine

    async def create_machines(
        self,
        machines: list[FlyMachine],
    ):
        created_machines = await asyncio.gather(
            *[self.create_machine(machine) for machine in machines]
        )

        return created_machines

    async def list_machines(
        self,
        regions: list[str] = [],
        ids_only: bool = False,
    ) -> list[FlyMachine] | list[str]:
        """
        Returns a list of machines that belong to a Fly application.

        Args:
            ids_only: If True, only machine IDs will be returned. Defaults to False.
        """
        r = await self._make_api_get_request(f"apps/{self.app_name}/machines")

        if r.status_code != 200:
            raise Exception(message=f"Unable to get machines in {self.app_name}!")

        machines = [FlyMachine(**machine) for machine in r.json()]

        if len(regions) > 0:
            machines = [machine for machine in machines if machine.region in regions]

        if ids_only is True:
            return [machine.id for machine in machines]

        return machines

    async def destroy_machines(
        self,
        machine_ids: list[str],
    ):
        """
        Destroys multiple Fly machines.

        Args:
            machine_ids (list[str]): A list of Fly machine IDs to destroy.
        """

        results = await asyncio.gather(
            *[self.Machine(machine_id).destroy() for machine_id in machine_ids]
        )

        return results

    def Machine(
        self,
        machine_id: str | None = None,
    ) -> Machine:
        return Machine(
            api_token=self.api_token,
            org_slug=self.org_slug,
            app_name=self.app_name,
            machine_id=machine_id,
        )

    ##################
    # Volume Methods #
    ##################

    def Volume(self, app_name) -> Volume:
        return Volume(
            api_token=self.api_token,
            org_slug=self.org_slug,
            app_name=app_name,
            machine_id=self.machine_id,
        )
