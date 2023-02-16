import logging
from datetime import datetime
from ipaddress import IPv6Address

from pydantic import BaseModel, validator

# FlyMachineConfig.checks


class FlyMachineConfigCheck(BaseModel):
    """Model for FlyMachineConfig.checks"""

    port: int
    type: str
    interval: str
    timeout: str
    method: str
    path: str


# FlyMachineConfig.guest


class FlyMachineConfigGuest(BaseModel):
    """Model for FlyMachineConfig.guest"""

    cpu_kind: str
    cpus: int
    memory_mb: int


# FlyMachineConfig.init


class FlyMachineConfigInit(BaseModel):
    """Model for FlyMachineConfig.init"""

    exec: str | None
    entrypoint: str | None
    cmd: str | None
    tty: bool


# FlyMachineConfig.mounts


class FlyMachineConfigMount(BaseModel):
    volume: str
    path: str


# FlyMachineConfig.processes


class FlyMachineConfigProcess(BaseModel):
    name: str
    entrypoint: list[str]
    cmd: list[str]
    env: dict[str, str]
    user: str | None = None


# FlyMachineConfig.services.port


class FlyMachineRequestConfigServicesPort(BaseModel):
    """Model for FlyMachineConfig.services.port"""

    port: int
    handlers: list[str]

    @validator("port")
    def validate_port(cls, port: int) -> int:
        assert port >= 0 and port <= 65536
        return port

    @validator("handlers")
    def validate_handlers(cls, handlers: list[str]) -> list[str]:
        logging.debug(handlers)
        # Only run validation if there is 1 or more handlers.
        if len(handlers) > 0:
            # Convert handlers to lowercase.
            handlers = [handler.casefold() for handler in handlers]
            assert (
                all(handler in ["http", "tcp", "tls", "udp"] for handler in handlers)
                is True
            )
        return handlers


# FlyMachineConfig.services


class FlyMachineConfigServices(BaseModel):
    """Model for FlyMachineConfig.services"""

    ports: list[FlyMachineRequestConfigServicesPort]
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


class FlyMachineConfig(BaseModel):
    env: dict[str, str] | None = None
    init: FlyMachineConfigInit | None = None
    image: str
    metadata: dict[str, str] | None = None
    restart: dict[str, str] | None = None
    services: list[FlyMachineConfigServices] | None = None
    guest: FlyMachineConfigGuest | None = None
    size: str = None
    metrics: None | dict[str, str | int]
    processes: list[FlyMachineConfigProcess] | None = None
    schedule: str | None = None
    mounts: list[FlyMachineConfigMount] | None = None
    checks: dict[str, FlyMachineConfigCheck] | None = None
    auto_destroy: bool = False


class FlyMachineImageRef(BaseModel):
    registry: str
    repository: str
    tag: str
    digest: str


class FlyMachineDetails(BaseModel):
    id: str
    name: str
    state: str
    region: str
    instance_id: str
    private_ip: IPv6Address
    config: FlyMachineConfig
    image_ref: FlyMachineImageRef
    created_at: datetime
    updated_at: datetime
