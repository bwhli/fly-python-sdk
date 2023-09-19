from datetime import datetime

from pydantic import BaseModel


class FlyVolume(BaseModel):
    attached_alloc_id: str
    attached_machine_id: str
    block_size: int
    blocks: int
    blocks_avail: int
    blocks_free: int
    created_at: datetime
    encrypted: bool
    fstype: str
    id: str
    name: str
    region: str
    size_gb: int
    state: str
    zone: str
