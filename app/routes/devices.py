from fastapi import APIRouter, HTTPException
from app.usbip import list_usb_devices
from app.serial_io import list_serial_devices

router = APIRouter()

@router.get("/usb")
def get_usb_devices():
    try:
        return {"devices": list_usb_devices()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/serial")
def get_serial_devices():
    try:
        return {"devices": list_serial_devices()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
def get_all_devices():
    try:
        return {
            "usb_devices": list_usb_devices(),
            "serial_devices": list_serial_devices()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
