from pydantic import BaseModel


class FlyAppDetails(BaseModel):
    name: str
    status: str
    organization: dict
