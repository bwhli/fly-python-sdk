from typing import TYPE_CHECKING

from fly_python_sdk.exceptions import AppInterfaceError
from fly_python_sdk.fly.machines import FlyMachine
from fly_python_sdk.models import FlyAppCreateRequest

if TYPE_CHECKING:
    from fly_python_sdk.fly import Fly


class FlyApp:
    def __init__(
        self,
        fly: "Fly",
        app_name: str,
    ):
        self.fly = fly
        self.app_name = app_name

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

        r = await self.fly._make_api_post_request("apps", app_details.model_dump())

        if r.status_code != 201:
            raise AppInterfaceError(
                message=f"Unable to create {self.app_name} in {org_slug}."
            )

        return

    def FlyMachine(self, machine_config):
        return FlyMachine(self, machine_config)
