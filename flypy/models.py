from datetime import datetime
from typing import Union

from pydantic import BaseModel

##################
# Fly App Models #
##################


class FlyAppDetailsResponse(BaseModel):
    name: str
    status: str
    organization: dict


######################
# Fly Machine Models #
######################


class FlyMachineDetailsConfigInit(BaseModel):
    exec: str | None
    entrypoint: str | None
    cmd: str | None
    tty: bool


class FlyMachineDetailsConfigGuest(BaseModel):
    cpu_kind: str
    cpus: int
    memory_mb: int


class FlyMachineDetailsConfig(BaseModel):
    env: dict[str, str] | None
    init: FlyMachineDetailsConfigInit
    image: str
    metadata: dict[str, str] | None
    restart: dict[str, str]
    guest: FlyMachineDetailsConfigGuest
    metrics: None | dict[str, str | int]
    auto_destroy: bool


class FlyMachineDetailsImageRef(BaseModel):
    registry: str
    repository: str
    tag: str
    digest: str
    labels: dict[str, str]


class FlyMachineDetailsEvent(BaseModel):
    id: str
    type: str
    status: str
    source: str
    timestamp: int


class FlyMachineDetailsResponse(BaseModel):
    id: str
    name: str
    state: str
    region: str
    instance_id: str
    private_ip: str
    config: FlyMachineDetailsConfig
    image_ref: FlyMachineDetailsImageRef
    created_at: datetime
    updated_at: datetime
    events: list[FlyMachineDetailsEvent]
