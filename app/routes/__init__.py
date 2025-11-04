# app/routes/__init__.py

from fastapi import APIRouter
from .dut import router as dut_router
from .devices import router as devices_router
from .serial_io import router as serial_router

router = APIRouter()

router.include_router(devices_router, prefix="/devices", tags=["devices"])
router.include_router(dut_router,     prefix="/dut",     tags=["dut"])
router.include_router(serial_router,  prefix="/serial",  tags=["serial"])
