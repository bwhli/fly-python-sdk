from fly_python_sdk.fly.api import FlyApi
from fly_python_sdk.fly.org import Org


class Fly(FlyApi):
    def Org(
        self,
        org_slug: str = "personal",
    ) -> "Org":
        return Org(
            api_token=self.api_token,
            org_slug=org_slug,
        )
