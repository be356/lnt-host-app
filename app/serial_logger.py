import os
import threading
import time
from datetime import datetime
from typing import Optional, TextIO

import serial
from dotenv import load_dotenv

load_dotenv()

SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/cu.usbmodemL1100WEU4")
SERIAL_BAUDRATE = int(os.getenv("SERIAL_BAUDRATE", "115200"))
LOG_DIR = os.getenv("LOG_DIR", "logs")

os.makedirs(LOG_DIR, exist_ok=True)


class SerialLogger:
    def __init__(self) -> None:
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._ser: Optional[serial.Serial] = None
        self._text_file: Optional[TextIO] = None
        self._vars_file: Optional[TextIO] = None
        self._current_job_id: Optional[str] = None

    def start(self, job_id: str, port: Optional[str] = None, baudrate: Optional[int] = None) -> str:
        if self._thread and self._thread.is_alive():
            return f"logger already running for job_id={self._current_job_id}"

        port = port or SERIAL_PORT
        baudrate = baudrate or SERIAL_BAUDRATE

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        base_name = f"{job_id}_{timestamp}"

        text_path = os.path.join(LOG_DIR, f"{base_name}_text.log")
        vars_path = os.path.join(LOG_DIR, f"{base_name}_vars.csv")

        self._ser = serial.Serial(port, baudrate, timeout=1)
        self._text_file = open(text_path, "a", encoding="utf-8")
        self._vars_file = open(vars_path, "a", encoding="utf-8")

        # CSV header for variables file
        self._vars_file.write("ts_utc,line\n")
        self._vars_file.flush()

        self._stop_event.clear()
        self._current_job_id = job_id

        self._thread = threading.Thread(
            target=self._run,
            name="SerialLoggerThread",
            daemon=True,
        )
        self._thread.start()

        return f"serial logging started (job_id={job_id}, port={port}, baud={baudrate})"

    def _run(self) -> None:
        assert self._ser is not None
        assert self._text_file is not None
        assert self._vars_file is not None

        while not self._stop_event.is_set():
            try:
                raw = self._ser.readline()
                if not raw:
                    continue

                line = raw.decode(errors="ignore").strip()
                if not line:
                    continue

                ts = datetime.utcnow().isoformat()

                # Text log (everything)
                self._text_file.write(f"[{ts}] {line}\n")
                self._text_file.flush()

                # Variables log (for now, whole line;
                # later we can parse key=value pairs)
                self._vars_file.write(f"{ts},{line}\n")
                self._vars_file.flush()
            except Exception:
                time.sleep(0.1)

    def stop(self) -> str:
        if not self._thread or not self._thread.is_alive():
            return "serial logger not running"

        self._stop_event.set()
        self._thread.join(timeout=2.0)

        if self._ser and self._ser.is_open:
            self._ser.close()
        if self._text_file:
            self._text_file.close()
        if self._vars_file:
            self._vars_file.close()

        job_id = self._current_job_id
        self._ser = None
        self._text_file = None
        self._vars_file = None
        self._thread = None
        self._current_job_id = None

        return f"serial logging stopped (job_id={job_id})"

    def status(self) -> dict:
        return {
            "running": bool(self._thread and self._thread.is_alive()),
            "job_id": self._current_job_id,
        }


serial_logger = SerialLogger()
