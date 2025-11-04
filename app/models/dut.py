from pydantic import BaseModel

class DutModel(BaseModel):
    id: str
    bus: str
    device: str
    vid: str
    pid: str
    description: str
    status: str = "idle"
