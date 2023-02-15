from flypy.exceptions import MachineInterfaceError
from flypy.fly import Fly
from flypy.models.machines import FlyMachineDetailsResponse


class FlyMachine(Fly):
    def __init__(self, api_token: str) -> None:
        super().__init__(api_token)

    def delete(
        self,
        app_name: str,
        machine_id: str,
    ) -> None:
        """Deletes a Fly.io machine.

        Args:
            app_name: The name of the new Fly.io app.
            machine_id: The id string for a Fly.io machine.
        """
        path = f"apps/{app_name}/machines/{machine_id}/start"
        r = self._make_api_delete_request(path)

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise MachineInterfaceError(
                message=f"Unable to delete {machine_id} in {app_name}!"
            )

        return

    def get(
        self,
        app_name: str,
        machine_id: str,
    ) -> FlyMachineDetailsResponse:
        """Returns information about a Fly.io machine.

        Args:
            app_name: The name of the new Fly.io app.
            machine_id: The id string for a Fly.io machine.
        """
        path = f"apps/{app_name}/machines/{machine_id}"
        r = self._make_api_get_request(path)

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise MachineInterfaceError(
                message=f"Unable to delete {machine_id} in {app_name}!"
            )

        return FlyMachineDetailsResponse(**r.json())

    def start(
        self,
        app_name: str,
        machine_id: str,
    ) -> None:
        """Starts a Fly.io machine.

        Args:
            app_name: The name of the new Fly.io app.
            machine_id: The id string for a Fly.io machine.
        """
        path = f"apps/{app_name}/machines/{machine_id}/start"
        r = self._make_api_post_request(path)

        # Raise an exception if HTTP status code is not 200.
        if r.status_code != 200:
            raise MachineInterfaceError(
                message=f"Unable to start {machine_id} in {app_name}!"
            )

        return
