"""
usbip.py — Device discovery helper for connected DUTs.

Purpose:
- Parse 'lsusb' command output to identify USB-connected Devices Under Test (DUTs).
- Designed for safe use (no root privileges required).
- Supports mock data injection for testing.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Callable, Iterable, List, Optional
import re
import subprocess

@dataclass(frozen=True)
class DUT:
    """Represent a single USB-connected DUT."""
    bus: str
    device: str
    vid: str
    pid: str
    description: str

    def as_dict(self) -> dict:
        """Convert DUT object into a dictionary for JSON serialization."""
        return asdict(self)

# Regex pattern that matches one line of `lsusb` output
_LSUSB_LINE = re.compile(
    r"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+):\s+ID\s+"
    r"(?P<vid>[0-9a-fA-F]{4}):(?P<pid>[0-9a-fA-F]{4})\s+(?P<desc>.+)$"
)

def _default_lsusb_provider() -> Iterable[str]:
    """
    Default provider: runs `lsusb` command.
    Returns each output line.
    If `lsusb` is not found or fails, returns empty list (safe fail).
    """
    try:
        output = subprocess.check_output(["lsusb"], text=True)
        return output.splitlines()
    except Exception:
        return []

def parse_lsusb_lines(lines: Iterable[str]) -> List[DUT]:
    """
    Parse raw lsusb output lines into a list of DUT objects.
    Each valid line becomes a DUT instance.
    """
    devices: List[DUT] = []
    for line in lines:
        match = _LSUSB_LINE.match(line.strip())
        if not match:
            continue  # skip invalid lines
        devices.append(
            DUT(
                bus=match.group("bus"),
                device=match.group("device"),
                vid=match.group("vid").lower(),
                pid=match.group("pid").lower(),
                description=match.group("desc").strip(),
            )
        )
    return devices

def list_duts(provider: Optional[Callable[[], Iterable[str]]] = None) -> List[DUT]:
    """
    Return a list of all connected DUTs.
    - provider: optional custom function returning mock lsusb lines for testing.
    """
    src = provider or _default_lsusb_provider
    return parse_lsusb_lines(src())
