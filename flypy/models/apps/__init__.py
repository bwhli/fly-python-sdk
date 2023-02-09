from pydantic import BaseModel


class FlyAppCreateRequest(BaseModel):
    app_name: str
    org_slug: str


class FlyAppDetailsResponse(BaseModel):
    name: str
    status: str
    organization: dict
