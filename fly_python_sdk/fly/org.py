

from fly_python_sdk.fly.api import FlyApi
from fly_python_sdk.fly.app import App
from fly_python_sdk.models import (
    FlyApps,
)


class Org(FlyApi):
    def __init__(
        self,
        api_token,
        org_slug: str = "personal",
    ):
        super().__init__(api_token)
        self.org_slug = org_slug

    def App(self, app_name) -> "App":
        return App(
            api_token=self.api_token,
            org_slug=self.org_slug,
            app_name=app_name,
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
