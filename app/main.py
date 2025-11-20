from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import os
import time
import requests

from .serial_logger import serial_logger

app = FastAPI(
    title="LNT Host App",
    description="Host-side API for discovering and talking to DUTs (proxied to Pi)",
    version="1.0.0",
)

# change this if your Pi IP changes
PI_HOST = os.getenv("PI_HOST", "http://192.168.1.78:8001")

# -------------------------------------------------
# MODELS
# -------------------------------------------------
class SerialTxRxRequest(BaseModel):
    dut_id: str
    data: str
    terminator: str | None = "\n"


class FlashRequest(BaseModel):
    dut_id: str
    firmware_path: str


class SerialLogStartRequest(BaseModel):
    job_id: str
    port: str | None = None
    baudrate: int | None = None


# -------------------------------------------------
# BASIC ROUTES
# -------------------------------------------------
@app.get("/")
def root():
    return RedirectResponse(url="/docs")


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy", "pi_host": PI_HOST}


@app.get("/version")
def version():
    return {"version": "1.0.0", "component": "lnt-host-app (proxy)"}


# -------------------------------------------------
# /duts (PROXIED TO PI)
# -------------------------------------------------
@app.get("/duts")
def get_duts():
    """
    Instead of listing USB locally (macOS Docker can't see USB),
    ask the Pi, which actually sees the devices.
    """
    try:
        resp = requests.get(f"{PI_HOST}/duts", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Could not reach Pi at {PI_HOST}: {e}")


# -------------------------------------------------
# SERIAL (optional stub — still local, can also be proxied)
# -------------------------------------------------
@app.post("/dut/serial/txrx")
def serial_txrx(req: SerialTxRxRequest):
    # if you want serial to go through the Pi too, call Pi here instead
    raise HTTPException(status_code=501, detail="serial/txrx not implemented on Mac container")


# -------------------------------------------------
# FLASH (optional stub)
# -------------------------------------------------
@app.post("/dut/flash")
def flash_dut(req: FlashRequest):
    raise HTTPException(status_code=501, detail="flash not implemented on Mac container")


# -------------------------------------------------
# SERIAL LOGGING (LOCAL LOGGER)
# -------------------------------------------------
@app.post("/serial/log/start")
def start_serial_log(req: SerialLogStartRequest):
    try:
        msg = serial_logger.start(
            job_id=req.job_id,
            port=req.port,
            baudrate=req.baudrate,
        )
        return {
            "ok": True,
            "message": msg,
            "status": serial_logger.status(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/serial/log/stop")
def stop_serial_log():
    msg = serial_logger.stop()
    return {
        "ok": True,
        "message": msg,
        "status": serial_logger.status(),
    }


@app.get("/serial/log/status")
def serial_log_status():
    return serial_logger.status()
