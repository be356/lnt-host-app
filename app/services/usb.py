from typing import List, Set
from serial.tools import list_ports
from ..core.config import settings
from ..models.dut import DutModel

def _parse_filters() -> Set[str]:
    if not settings.DEVICE_FILTERS:
        return set()
    return {f.strip().lower() for f in settings.DEVICE_FILTERS.split(",") if f.strip()}

def list_duts() -> List[DutModel]:
    # MOCK mode for development without hardware
    if settings.MOCK_DUTS:
        return [
            DutModel(
                id="mock-tty-usbmodem1234",
                bus="usb",
                device="/dev/tty.usbmodem1234",
                vid="0451",
                pid="bef3",
                description="TI XDS110 Debug Probe (MOCK)",
                status="idle",
            )
        ]

    filters = _parse_filters()
    duts: List[DutModel] = []
    for p in list_ports.comports():
        vid = f"{p.vid:04x}" if p.vid is not None else "0000"
        pid = f"{p.pid:04x}" if p.pid is not None else "0000"
        if filters and f"{vid}:{pid}" not in filters:
            continue
        desc = p.description or p.product or "USB Serial Device"
        devpath = p.device
        duts.append(
            DutModel(
                id=devpath.replace("/", "_"),
                bus="usb",
                device=devpath,
                vid=vid,
                pid=pid,
                description=desc,
                status="idle",
            )
        )
    return duts
