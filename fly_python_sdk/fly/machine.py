import logging

from fly_python_sdk import FLY_MACHINE_DEFAULT_WAIT_TIMEOUT, FLY_MACHINE_STATES
from fly_python_sdk.fly.api import FlyApi
from fly_python_sdk.models import FlyMachine, FlyMachineConfig


class Machine(FlyApi):
    def __init__(
        self,
        api_token,
        org_slug,
        app_name,
        machine_id: str,
    ):
        super().__init__(api_token)
        self.org_slug = org_slug
        self.app_name = app_name
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

    async def destroy(
        self,
        wait_for_target_state: bool = True,
    ) -> None:
        """Destroys a Fly machine.

        Args:
            wait_for_target_state (bool): If True, the function will wait for the machine to enter the "destroyed" state before returning. Defaults to True.
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
        if wait_for_target_state is True:
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

    async def start(
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

    async def stop(
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
