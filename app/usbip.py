import subprocess, json, re

def list_duts():
    """
    Parse `lsusb` to produce a list of connected devices.
    Marks TI 0451:bef3 explicitly as 'ti-launchpad' when present.
    """
    try:
        res = subprocess.run(["lsusb"], capture_output=True, text=True, check=False)
        duts = []
        for line in res.stdout.splitlines():
            m = re.search(r'ID\s+([0-9a-f]{4}):([0-9a-f]{4})', line, re.I)
            if not m: 
                continue
            vid, pid = m.group(1).lower(), m.group(2).lower()
            desc = "USB Device"
            if vid == "0451" and pid == "bef3":
                desc = "TI CC1352 LaunchPad"
            duts.append({"id": f"{vid}:{pid}", "description": desc, "status": "connected"})
        return duts
    except Exception as e:
        return {"error": str(e)}
def list_duts_internal():
    # temporary stub so FastAPI can import it
    # later we can make this run `usbip list` on the Pi
    return []
def list_duts_internal():
    return []
