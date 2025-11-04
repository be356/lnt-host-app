from pydantic import BaseModel
from typing import Optional

class DutInternal(BaseModel):
    id: str
    vendor_id: Optional[str]
    product_id: Optional[str]
    serial: Optional[str]
    bus: Optional[str]
    device: Optional[str]
    port: Optional[str]
    tty: Optional[str]
    description: Optional[str]

class DutPublic(BaseModel):
    id: str
    bus: Optional[str] = None
    device: Optional[str] = None
    vid: Optional[str] = None
    pid: Optional[str] = None
    description: Optional[str] = None
    status: str = "idle"
