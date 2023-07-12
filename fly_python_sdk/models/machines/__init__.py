from typing import Optional

from pydantic import BaseModel, validator

from fly_python_sdk.constants import (
    FLY_MACHINE_DEFAULT_CPU_COUNT,
    FLY_MACHINE_DEFAULT_MEMORY_MB,
)


class FlyMachineConfigTcpCheck(BaseModel):
    type: str = "tcp"
    port: int
    interval: int
    timeout: int


class FlyMachineConfigHttpCheck(BaseModel):
    type: str = "http"
    port: int
    interval: int
    timeout: int
    method: str = "GET"
    path: str
    protocol: str = "http"
    tls_skip_verify: bool = False
    headers: Optional[dict[str, str]] = None


class FlyMachineConfigGuest(BaseModel):
    cpus: int = FLY_MACHINE_DEFAULT_CPU_COUNT
    memory_mb: int = FLY_MACHINE_DEFAULT_MEMORY_MB
    kernel_args: Optional[list[str]] = None


class FlyMachineConfigServicesConcurrency(BaseModel):
    type: Optional[str] = None
    soft_limit: Optional[int] = None
    hard_limit: Optional[int] = None


class FlyMachineConfigMetrics(BaseModel):
    port: int
    path: str


class FlyMachineConfigMount(BaseModel):
    volume: str
    path: str


class FlyMachineConfigServicesPort(BaseModel):
    port: Optional[int] = None
    handlers: Optional[list[str]] = None


class FlyMachineConfigProcess(BaseModel):
    name: str
    entrypoint: list[str]
    cmd: list[str]
    env: Optional[dict[str, str]] = None
    user: Optional[str] = None


class FlyMachineConfigServices(BaseModel):
    protocol: str
    concurrency: Optional[FlyMachineConfigServicesConcurrency] = None
    internal_port: int


class FlyMachineConfig(BaseModel):
    image: str
    guest: Optional[FlyMachineConfigGuest] = None
    auto_destroy: Optional[bool] = None
    size: Optional[str] = None
    env: Optional[dict[str, str]] = None
    ports: Optional[list[FlyMachineConfigServicesPort]] = None
    processes: Optional[list[FlyMachineConfigProcess]] = None
    schedule: Optional[str] = None
    mounts: Optional[FlyMachineConfigMount] = None
    metrics: Optional[FlyMachineConfigMetrics] = None
    checks: Optional[list[FlyMachineConfigHttpCheck | FlyMachineConfigTcpCheck]] = None


class FlyMachine(BaseModel):
    name: Optional[str]
    region: Optional[str]
    config: FlyMachineConfig
