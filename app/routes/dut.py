from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
import os
from app.dut import build_flash_cmd, run_command, FlashError

router = APIRouter()

class FlashRequest(BaseModel):
    firmware: str = Field(..., description="Path to .bin/.out/.elf")
    port: Optional[str] = Field(default=None, description="Optional serial/JTAG port")
    tool: Optional[Literal["dslite","openocd"]] = Field(default=None)
    dry_run: bool = Field(default=True, description="If true, only return the command")

class FlashResponse(BaseModel):
    dry_run: bool
    command: list
    executed: bool
    result: Optional[Dict[str, Any]] = None

@router.post("/flash", response_model=FlashResponse)
def flash(req: FlashRequest):
    try:
        cmd = build_flash_cmd(tool=req.tool or os.getenv("FLASH_TOOL"),
                              port=req.port, firmware=req.firmware)
    except FlashError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    allow = os.getenv("ALLOW_FLASH","0").lower() in ("1","true","yes")
    if req.dry_run or not allow:
        return FlashResponse(dry_run=True, command=cmd, executed=False, result=None)

    result = run_command(cmd)
    if not result["ok"]:
        raise HTTPException(status_code=500, detail=result["stderr"] or "Flash failed")
    return FlashResponse(dry_run=False, command=cmd, executed=True, result=result)
