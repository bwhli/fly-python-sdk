from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from fly_python_sdk import FLY_MACHINE_DEFAULT_CPU_COUNT, FLY_MACHINE_DEFAULT_MEMORY_MB

# Apps


class FlyAppCreateRequest(BaseModel):
    app_name: str
    org_slug: str


class FlyAppDetailsResponse(BaseModel):
    name: str
    status: str
    organization: dict


# Machines


class FlyMachineConfigTcpCheck(BaseModel):
    type: str = "tcp"
    port: int
    interval: int | str
    timeout: int | str


class FlyMachineConfigHttpCheck(BaseModel):
    type: str = "http"
    port: int
    interval: int | str
    timeout: int | str
    method: str = "GET"
    path: str
    protocol: str = "http"
    tls_skip_verify: bool = False
    headers: Optional[dict[str, str]] = None


class FlyMachineConfigGuest(BaseModel):
    cpu_kind: str
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


class FlyMachineConfigInit(BaseModel):
    exec: Optional[str] = None
    entrypoint: Optional[str] = None
    cmd: Optional[str] = None
    tty: Optional[bool] = None


class FlyMachineConfigRestart(BaseModel):
    policy: Optional[str] = None


class FlyMachineImageRef(BaseModel):
    registry: str
    repository: str
    tag: str
    digest: str
    labels: Optional[dict[str, str]] = None


class FlyMachineConfig(BaseModel):
    env: Optional[dict[str, str]] = None
    init: Optional[FlyMachineConfigInit] = None
    image: str
    metadata: Optional[dict[str, str]] = None
    restart: Optional[FlyMachineConfigRestart] = None
    guest: Optional[FlyMachineConfigGuest] = None
    auto_destroy: Optional[bool] = None
    size: Optional[str] = None
    env: Optional[dict[str, str]] = None
    ports: Optional[list[FlyMachineConfigServicesPort]] = None
    processes: Optional[list[FlyMachineConfigProcess]] = None
    schedule: Optional[str] = None
    mounts: Optional[FlyMachineConfigMount] = None
    metrics: Optional[FlyMachineConfigMetrics] = None
    checks: Optional[dict[str, FlyMachineConfigHttpCheck | FlyMachineConfigTcpCheck]] = None  # fmt: skip


class FlyMachineEventRequest(BaseModel):
    exit_event: dict
    restart_count: int


class FlyMachineEvent(BaseModel):
    type: str
    status: str
    request: Optional[FlyMachineEventRequest] = None
    source: str
    timestamp: datetime


class FlyMachine(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    state: Optional[str] = None
    region: Optional[str] = None
    instance_id: Optional[str] = None
    private_ip: Optional[str] = None
    config: FlyMachineConfig
    image_ref: Optional[FlyMachineImageRef] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
