from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# if these imports fail we just stub them so container doesn't crash
try:
    from .usbip import list_duts_internal
except Exception:
    def list_duts_internal():
        return []

try:
    from .serial_io import SerialPort
except Exception:
    SerialPort = None

app = FastAPI(
    title="LNT Host App",
    description="Host-side API for discovering and talking to DUTs",
    version="1.0.0",
)

# send root (what Docker opens) straight to Swagger
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.get("/duts")
async def get_duts():
    return {"duts": list_duts_internal()}
