from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from flypy.constants import FLY_REGIONS

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


class FlyMachineDetailsRequestConfigServicesPort(BaseModel):
    port: int
    handlers: list[str]

    @validator("port")
    def validate_port(cls, port: int) -> int:
        assert port >= 0 and port <= 65536
        return port

    @validator("handlers")
    def validate_handlers(cls, handlers: list[str]) -> list[str]:
        # Only run validation if there is 1 or more handlers.
        if len(handlers) > 0:
            # Convert handlers to lowercase.
            handlers = [handler.casefold() for handler in handlers]
            assert (
                all(handler in ["http", "tcp", "udp"] for handler in handlers) is True
            )
        return handlers


class FlyMachineDetailsRequestConfigService(BaseModel):
    ports: list[FlyMachineDetailsRequestConfigServicesPort]
    protocol: str
    internal_port: int

    @validator("internal_port")
    def validate_internal_port(cls, internal_port: int) -> int:
        assert internal_port >= 0 and internal_port <= 65536
        return internal_port

    @validator("protocol")
    def validate_protocol(cls, protocol: str) -> str:
        assert protocol in ["http", "tcp", "udp"]
        return protocol


class FlyMachineDetailsRequestCheck(BaseModel):
    type: str
    port: int
    method: str
    path: str
    interval: str
    timeout: str


class FlyMachineDetailsRequestGuest(BaseModel):
    cpus: int
    memory_mb: int
    kernal_args: list[str]


class FlyMachineDetailsRequestProcess(BaseModel):
    name: str
    entrypoint: list[str]
    cmd: list[str]
    env: dict[str, str]
    user: Optional[str]


class FlyMachineDetailsRequestMount(BaseModel):
    volume: str
    path: str


class FlyMachineDetailsRequestConfig:
    image: str
    guest: FlyMachineDetailsRequestGuest
    size: str
    env: dict[str, str] | None
    services: list[FlyMachineDetailsRequestConfigService]
    checks: dict[str, FlyMachineDetailsRequestCheck]
    processes: list[FlyMachineDetailsRequestProcess]
    schedule: Optional[str]
    mounts: Optional[list[FlyMachineDetailsRequestMount]]
    checks: Optional[dict[str, FlyMachineDetailsRequestCheck]]


class FlyMachineDetailsRequest(BaseModel):
    name: str
    config: FlyMachineDetailsRequestConfig
