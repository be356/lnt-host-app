"""
Unit tests for app.usbip (no hardware required).
"""
from app.usbip import parse_lsusb_lines, list_duts, DUT

def test_parse_lsusb_lines_basic():
    lines = [
        "Bus 001 Device 003: ID 0451:bef3 Texas Instruments, Inc. CC1352R1 Launchpad",
        "Bus 002 Device 007: ID 1234:ABCD Example Device Inc.",
    ]
    devices = parse_lsusb_lines(lines)
    assert len(devices) == 2
    assert devices[0] == DUT(
        bus="001", device="003", vid="0451", pid="bef3",
        description="Texas Instruments, Inc. CC1352R1 Launchpad"
    )
    assert devices[1] == DUT(
        bus="002", device="007", vid="1234", pid="abcd",
        description="Example Device Inc."
    )

def test_parse_skips_invalid_lines():
    lines = [
        "garbage line that should be ignored",
        "Bus 003 Device 010: ID 046d:c534 Logitech, Inc. Unifying Receiver",
    ]
    devices = parse_lsusb_lines(lines)
    assert len(devices) == 1
    assert devices[0].bus == "003"
    assert devices[0].device == "010"
    assert devices[0].vid == "046d"
    assert devices[0].pid == "c534"

def test_list_duts_with_mock_provider():
    mock_lines = [
        "Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub",
        "Bus 001 Device 003: ID 0451:bef3 Texas Instruments, Inc. CC1352R1 Launchpad",
    ]
    devices = list_duts(provider=lambda: mock_lines)
    assert [d.vid for d in devices] == ["1d6b", "0451"]
    assert devices[1].description.endswith("CC1352R1 Launchpad")

def test_default_provider_handles_missing_lsusb(monkeypatch):
    import app.usbip as usbip
    def boom(*a, **k):
        raise FileNotFoundError("lsusb not found")
    monkeypatch.setattr(usbip.subprocess, "check_output", boom)
    # Should not raise; should return empty list
    devices = usbip.list_duts()
    assert devices == []
