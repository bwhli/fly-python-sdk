from fly_python_sdk.fly.api import FlyApi
from fly_python_sdk.fly.org import Org


class Fly(FlyApi):
    def __init__(
        self,
        api_token: str,
    ):
        super().__init__(api_token)

    def Org(
        self,
        org_slug: str = "personal",
    ) -> "Org":
        return Org(
            api_token=self.api_token,
            org_slug=org_slug,
        )
