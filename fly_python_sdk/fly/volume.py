from fly_python_sdk.fly.api import FlyApi


class Volume(FlyApi):
    """
    A class for interacting with Fly.io Volumes.
    """

    def __init__(
        self,
        api_token,
        org_slug,
        app_name,
        machine_id: str,
        volume_id: str,
    ):
        super().__init__(api_token)
        self.org_slug = org_slug
        self.app_name = app_name
        self.machine_id = machine_id
        self.volume_id = volume_id
