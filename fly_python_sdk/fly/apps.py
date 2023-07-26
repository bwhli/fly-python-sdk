from typing import TYPE_CHECKING

from fly_python_sdk.fly.machines import FlyMachine

if TYPE_CHECKING:
    from fly_python_sdk.fly import Fly


class FlyApp:
    def __init__(
        self,
        fly: Fly,
        app_name: str,
    ):
        self.fly = fly
        self.app_name = app_name

    async def create(
        self,
        network: str = "default",
        org_slug: str = "personal",
    ):
        pass
        # The logic for creating an app using REST API calls.

    def FlyMachine(self, machine_config):
        return FlyMachine(self, machine_config)
