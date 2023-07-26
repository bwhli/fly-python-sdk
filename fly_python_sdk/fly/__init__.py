from fly_python_sdk import DEFAULT_API_TIMEOUT, FLY_MACHINES_API_DEFAULT_API_HOSTNAME
from fly_python_sdk.fly.apps import FlyApp


class Fly:
    def __init__(
        self,
        api_token: str,
        base_url: str = FLY_MACHINES_API_DEFAULT_API_HOSTNAME,
        api_timeout: int = DEFAULT_API_TIMEOUT,
    ):
        self.api_token = api_token
        self.base_url = base_url
        self.api_timeout = api_timeout

    def FlyApp(self, app_name):
        return FlyApp(self, app_name)
