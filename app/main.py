from dotenv import load_dotenv
load_dotenv()

import os, subprocess
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .models import DutPublic, DutInternal
from .usbip import list_duts_internal
from .serial_io import SerialPort

app = FastAPI(title="LNT Host App", version="0.2.0")

# --- models ---
class SerialTxRxRequest(BaseModel):
    dut_id: str
    data: str
    terminator: str = ""     # e.g. "", "\n", "\r", "\r\n"
    wait_ms: int = 300       # how long to wait after write before reading
    baud: Optional[int] = None

class SerialTxRxResponse(BaseModel):
    dut_id: str
    sent: str
    read: str

# --- helpers ---
def _to_public(d: DutInternal) -> DutPublic:
    vid = d.vendor_id[2:] if d.vendor_id and d.vendor_id.startswith("0x") else d.vendor_id
    pid = d.product_id[2:] if d.product_id and d.product_id.startswith("0x") else d.product_id
    return DutPublic(
        id=d.id, bus=d.bus, device=d.device, vid=vid, pid=pid,
        description=d.description or (f"USB {vid}:{pid}" if vid and pid else None),
        status="idle",
    )

def _guess_tty() -> Optional[str]:
    for pat in ("tty.usbmodem*", "tty.usbserial*", "ttyACM*", "ttyUSB*"):
        out = os.popen(f"ls -1 /dev/{pat} 2>/dev/null | head -n1").read().strip()
        if out:
            return out
    return None

def _resolve_tty(dut_id: str) -> str:
    env_tty = os.getenv("SERIAL_PORT")
    if env_tty and os.path.exists(env_tty):
        return env_tty
    tty = _guess_tty()
    if tty:
        return tty
    raise HTTPException(status_code=404, detail=f"No serial TTY found for {dut_id}. Set SERIAL_PORT in .env.")

# --- routes ---
@app.get("/health")
def health(): return "OK"

@app.get("/version")
def version(): return app.version

@app.get("/duts", response_model=List[DutPublic])
def get_duts():
    internals = list_duts_internal()
    return [_to_public(d) for d in internals]

@app.post("/dut/serial/txrx", response_model=SerialTxRxResponse)
def serial_txrx(req: SerialTxRxRequest):
    port = _resolve_tty(req.dut_id)
    baud = req.baud or int(os.getenv("SERIAL_BAUD", "115200"))
    payload = (req.data + req.terminator).encode("utf-8")
    with SerialPort(port, baud=baud) as sp:
        sp.write(payload)
        out = sp.read_for_ms(req.wait_ms)
    return SerialTxRxResponse(dut_id=req.dut_id, sent=(req.data + req.terminator), read=out)


from pydantic import BaseModel

class FlashRequest(BaseModel):
    dut_id: str
    firmware_path: str

class FlashResponse(BaseModel):
    dut_id: str
    ok: bool
    stdout: str
    stderr: str
    exit_code: int

@app.post("/dut/flash", response_model=FlashResponse)
def flash(req: FlashRequest):
    cmd = os.getenv("FLASH_CMD", "").strip()
    if not cmd:
        raise HTTPException(status_code=500, detail="FLASH_CMD not set in .env")
    env = dict(os.environ)
    env["DUT_ID"] = req.dut_id
    env["FIRMWARE_PATH"] = req.firmware_path
    cp = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
    return FlashResponse(
        dut_id=req.dut_id,
        ok=(cp.returncode == 0),
        stdout=cp.stdout.strip(),
        stderr=cp.stderr.strip(),
        exit_code=cp.returncode
    )
