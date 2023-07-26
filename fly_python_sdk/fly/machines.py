from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fly_python_sdk.fly.apps import FlyApp


class FlyMachine:
    def __init__(
        self,
        app: FlyApp,
        machine_config,
    ):
        self.app = app
        self.machine_config = machine_config

    async def create(self):
        """Creates a new machine within the app."""
        # The logic for creating a machine within the app using REST API calls.
        pass
