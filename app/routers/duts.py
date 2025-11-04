from fastapi import APIRouter
from typing import List
from ..models.dut import DutModel
from ..services.usb import list_duts

router = APIRouter()

@router.get("/duts", response_model=List[DutModel])
def get_duts():
    return list_duts()
