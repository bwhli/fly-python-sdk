from flypy.exceptions import AppInterfaceError
from flypy.fly import Fly
from flypy.models.apps import FlyAppCreateRequest, FlyAppDetailsResponse
from flypy.models.machines import FlyMachineDetailsResponse


class FlyApp(Fly):
    def __init__(self, api_token: str) -> None:
        super().__init__(api_token)

    def create(
        self,
        app_name: str,
        org_slug: str,
    ) -> None:
        """Creates a new app on Fly.io.

        Args:
            app_name: The name of the new Fly.io app.
            org_slug: The slug of the organization to create the app within.
        """
        path = "apps"
        app_details = FlyAppCreateRequest(app_name=app_name, org_slug=org_slug)
        r = self._make_api_post_request(path, app_details.dict())

        # Raise an exception if HTTP status code is not 201.
        if r.status_code != 201:
            raise AppInterfaceError(
                message=f"Unable to create {app_name} in {org_slug}!"
            )

        return

    def get(
        self,
        app_name: str,
    ) -> FlyAppDetailsResponse:
        """Returns information about a Fly.io application.

        Args:
            app_name: The name of the new Fly.io app.
        """
        path = f"apps/{app_name}"
        r = self._make_api_get_request(path)

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise AppInterfaceError(message=f"Unable to get {app_name}!")

        return FlyAppDetailsResponse(**r.json())

    def list_machines(
        self,
        app_name: str,
        ids_only: bool = False,
    ) -> list[FlyMachineDetailsResponse]:
        """Returns a list of machines that belong to a Fly.io application.

        Args:
            ids_only: If True, only machine IDs will be returned. Defaults to False.
        """
        path = f"apps/{app_name}/machines"
        r = self._make_api_get_request(path)

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise AppInterfaceError(message=f"Unable to get machines in {app_name}!")

        # Create a FlyMachineDetailsResponse object for each machine.
        machines = [FlyMachineDetailsResponse(**machine) for machine in r.json()]

        # Filter and return a list of ids if ids_only is True.
        if ids_only is True:
            return [machine.id for machine in machines]

        return machines
