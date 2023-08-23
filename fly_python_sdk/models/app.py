from pydantic import BaseModel

from fly_python_sdk.models.org import FlyOrg


class FlyApp(BaseModel):
    name: str
    organization: FlyOrg
    status: str


class FlyAppDetailsResponse(BaseModel):
    name: str
    status: str
    organization: dict


class FlyApps(BaseModel):
    apps: list["FlyAppsAppOverview"]
    total_apps: int


class FlyAppsAppOverview(BaseModel):
    machine_count: int
    name: str
    network: str
