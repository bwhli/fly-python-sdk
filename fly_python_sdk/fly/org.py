from fly_python_sdk.exceptions import FlyError
from fly_python_sdk.fly.api import FlyApi
from fly_python_sdk.fly.app import App
from fly_python_sdk.models.app import FlyApps


class Org(FlyApi):
    """
    A class for interacting with Fly.io Organizations.
    """

    def __init__(
        self,
        api_token,
        org_slug: str = "personal",
    ):
        super().__init__(api_token)
        self.org_slug = org_slug

    ###############
    # App Methods #
    ###############

    async def create_app(
        self,
        app_name: str,
        network: str = "default",
    ):
        """Creates a new app on Fly.

        Args:
            app_name: The name of the new Fly app.
            org_slug: The slug of the organization to create the app within.
        """

        payload = {
            "app_name": app_name,
            "network": network,
            "org_slug": self.org_slug,
        }

        r = await self._make_api_post_request(
            "apps",
            payload,
        )

        if r.status_code != 201:
            raise FlyError(message=f"Unable to create {app_name} in {self.org_slug}.")

        return

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
            raise FlyError(
                "Invalid sort_by value. Valid sort_by values are 'machine_count', 'name', and 'network'."
            )

        r = await self._make_api_get_request(f"apps?org_slug={self.org_slug}")

        if r.status_code != 200:
            raise FlyError(
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

    def App(self, app_name) -> "App":
        return App(
            api_token=self.api_token,
            org_slug=self.org_slug,
            app_name=app_name,
        )
