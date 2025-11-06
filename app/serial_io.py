import glob, os, time
import serial
from dotenv import load_dotenv

load_dotenv()
BAUD = int(os.getenv("SERIAL_BAUD", "115200"))

def _guess_serial_port():
    # macOS typical device names
    candidates = sorted(glob.glob("/dev/tty.usbmodem*")) + sorted(glob.glob("/dev/tty.usbserial*"))
    # Linux fallback if you run on Pi later
    candidates += sorted(glob.glob("/dev/ttyACM*")) + sorted(glob.glob("/dev/ttyUSB*"))
    return candidates[0] if candidates else None

def serial_txrx(dut_id: str, data: str, terminator: str = "\n"):
    port = _guess_serial_port()
    if not port:
        return {"error": "No serial port found (looked for tty.usbmodem/usbserial/ACM/USB)"}
    try:
        with serial.Serial(port, BAUD, timeout=1) as ser:
            ser.write((data + terminator).encode())
            time.sleep(0.2)
            line = ser.readline().decode(errors="ignore").strip()
            return {"port": port, "baud": BAUD, "sent": data, "received": line}
    except Exception as e:
        return {"error": str(e)}
class SerialPort:
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 115200):
        # placeholder, real code would open pyserial here
        self.port = port
        self.baudrate = baudrate

    def write(self, data: str):
        # placeholder for sending to DUT
        return f"sent: {data}"

    def read(self):
        # placeholder for reading from DUT
        return "ok"

def list_serial_ports():
    # placeholder, main.py may call this
    return []
