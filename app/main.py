from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI(
    title="LNT Host App",
    description="Host-side API for discovering and talking to DUTs",
    version="1.0.0",
)

# MODELS
class SerialTxRxRequest(BaseModel):
    dut_id: str
    data: str
    terminator: str | None = None

class FlashRequest(BaseModel):
    dut_id: str
    firmware_path: str

# ROOT → docs
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/version")
async def version():
    return {"version": "1.0.0", "component": "lnt-host-app"}

@app.get("/duts")
async def get_duts():
    # later: call usbip / discovery
    return {"duts": []}

@app.post("/dut/serial/txrx")
async def serial_txrx(body: SerialTxRxRequest):
    # stub for now
    return {
        "dut_id": body.dut_id,
        "data_sent": body.data,
        "terminator": body.terminator,
        "response": "OK (stub)"
    }

@app.post("/dut/flash")
async def flash_dut(body: FlashRequest):
    # stub for now
    return {
        "dut_id": body.dut_id,
        "firmware_path": body.firmware_path,
        "status": "flash-started (stub)"
    }

# ROUTES
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/version")
async def version():
    return {"version": "1.0.0", "component": "lnt-host-app"}

@app.get("/duts")
async def get_duts():
    # later: call usbip / discovery
    return {"duts": []}

@app.post("/dut/serial/txrx")
async def serial_txrx(body: SerialTxRxRequest):
    # stub for now
    return {
        "dut_id": body.dut_id,
        "data_sent": body.data,
        "terminator": body.terminator,
        "response": "OK (stub)"
    }

@app.post("/dut/flash")
async def flash_dut(body: FlashRequest):
    # stub for now
    return {
        "dut_id": body.dut_id,
        "firmware_path": body.firmware_path,
        "status": "flash-started (stub)"
    }

