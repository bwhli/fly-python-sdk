from pydantic import BaseModel


class FlyOrg(BaseModel):
    name: str
    slug: str
