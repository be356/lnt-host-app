# app/dut.py
import os
import shlex
import subprocess
from pathlib import Path
from typing import List, Dict, Any

class FlashError(Exception):
    pass

def _assert_file(path: str) -> Path:
    p = Path(path).expanduser().resolve()
    if not p.exists() or not p.is_file():
        raise FlashError(f"Firmware not found: {p}")
    return p

def build_flash_cmd(tool: str | None, port: str | None, firmware: str) -> List[str]:
    """
    Build a flashing command. Supports DSLite (TI) or OpenOCD via env.
    Env:
      FLASH_TOOL = 'dslite' | 'openocd'
      DSLITE_PATH (optional)  e.g. /Applications/ti/ccs2031/ccs/ccs_base/DebugServer/bin/DSLite
      CCXML_PATH (required for dslite)
      OPENOCD_PATH (optional) e.g. /usr/local/bin/openocd
      OPENOCD_CFG (required for openocd) e.g. interface/xds110.cfg,target/cc13x2.cfg
    """
    fw = _assert_file(firmware)
    which = (tool or os.getenv("FLASH_TOOL") or "dslite").lower()

    if which == "dslite":
        dslite = os.getenv("DSLITE_PATH", "DSLite")
        ccxml  = os.getenv("CCXML_PATH")
        if not ccxml:
            raise FlashError("CCXML_PATH env not set for DSLite.")
        return [dslite, "load", "-c", ccxml, "-f", str(fw)]

    if which == "openocd":
        openocd = os.getenv("OPENOCD_PATH", "openocd")
        cfgs = os.getenv("OPENOCD_CFG")
        if not cfgs:
            raise FlashError("OPENOCD_CFG env not set for OpenOCD.")
        args: list[str] = []
        for c in cfgs.split(","):
            args += ["-f", c]
        return [openocd, *args, "-c", f"program {shlex.quote(str(fw))} verify reset exit"]

    raise FlashError(f"Unknown FLASH_TOOL '{which}'")

def run_command(cmd: List[str], timeout: int = 180) -> Dict[str, Any]:
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
