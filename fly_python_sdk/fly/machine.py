import logging

from fly_python_sdk.exceptions import FlyError
from fly_python_sdk.fly.api import FlyApi
from fly_python_sdk.models.machine import FlyMachine, FlyMachineEvent


class Machine(FlyApi):
    """
    A class for interacting with Fly.io Machines.
    """

    def __init__(
        self,
        api_token,
        org_slug,
        app_name,
        machine_id: str | None = None,
    ):
        super().__init__(api_token)
        self.org_slug = org_slug
        self.app_name = app_name
        self.machine_id = machine_id

    ###################
    # MACHINE METHODS #
    ###################

    ################
    # Base Methods #
    ################

    async def destroy(
        self,
    ) -> None:
        """
        Destroys a Fly machine.
        """
        r = await self._make_api_delete_request(
            f"apps/{self.app_name}/machines/{self.machine_id}"
        )

        if r.status_code != 200:
            raise FlyError(
                message=f"Unable to delete {self.machine_id} in {self.app_name}!"
            )

        return

    async def inspect(
        self,
    ) -> FlyMachine:
        """
        Get information about a Fly machine.

        Args:
            app_name: The name of the new Fly app.
            machine_id: The id string for a Fly machine.
        """
        if not self.machine_id:
            raise FlyError(
                message="Please provide the ID of the Machine you want to inspect."
            )

        r = await self._make_api_get_request(
            f"apps/{self.app_name}/machines/{self.machine_id}"
        )

        if r.status_code != 200:
            raise FlyError(
                message=f"Unable to get {self.machine_id} in {self.app_name}!"
            )

        return FlyMachine(**r.json())

    async def start(
        self,
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
            raise FlyError(
                message=f"Unable to start {self.machine_id} in {self.app_name}!"
            )

        return

    async def stop(
        self,
    ) -> None:
        """Stop a Fly machine.

        Args:
            app_name: The name of the new Fly app.
            machine_id: The id string for a Fly machine.
        """
        machine = await self.get_machine(self.app_name, self.machine_id)

        # Return if the machine is already stopped.
        if machine.state == "stopped":
            return

        logging.info(f"Attemping to stop {self.machine_id} in {self.app_name}.")

        r = await self._make_api_post_request(
            f"apps/{self.app_name}/machines/{self.machine_id}/stop"
        )

        if r.status_code != 200:
            raise FlyError(
                message=f"Unable to stop {self.machine_id} in {self.app_name}!"
            )

        logging.info(f"Stopped {self.machine_id} in {self.app_name}.")

        return

    #################
    # Event Methods #
    #################

    async def get_events(
        self,
    ) -> list[FlyMachineEvent]:
        """
        Returns a list of events for a Fly machine.
        """

        r = await self._make_api_get_request(
            f"apps/{self.app_name}/machines/{self.machine_id}/events"
        )

        events = [FlyMachineEvent(**event) for event in r.json()]

        return events

    ###################
    # Utility Methods #
    ###################

    async def clone(
        self,
        name: str | None = None,
        region: str | None = None,
    ):
        """
        Clone a Fly machine.

        Args:
            name (str): The name of the new Fly machine. Defaults to None.
            region (str): The region to create the new Fly machine in. Defaults to None.
        """
        source_machine = await self.inspect()

        if region is None:
            region = source_machine.region

        new_machine = FlyMachine(
            name=name,
            region=region,
            config=source_machine.config,
        )

        r = await self._make_api_post_request(
            f"apps/{self.app_name}/machines",
            payload=new_machine.model_dump(exclude_none=True),
        )

        return FlyMachine(**r.json())
