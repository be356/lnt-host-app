# 🧠 LNT Host App

The **LNT Host App** runs on a Raspberry Pi and bridges communication between the **LNT control system** and **Device Under Test (DUT)** hardware. It uses **Docker**, **USB/IP**, and **Serial communication** to enable remote testing, monitoring, and firmware flashing.

---

## 🧩 Overview
- Runs as a **FastAPI** backend inside a Docker container on Raspberry Pi 4/5  
- Connects to DUTs through **USB/IP** and **Serial** interfaces  
- Exposes REST **API endpoints** for Jenkins, GUI, or CLI tools  
- Multiple Pis can be networked together for distributed testing environments  

---

## 🧰 Requirements

### 🖥️ Hardware
- Raspberry Pi 4 or 5 (2GB+)
- MicroSD card (32GB+)
- Power supply (5V 3A)
- USB cable connecting Pi to DUT
- DUT hardware board
- Wi-Fi or Ethernet connection
- *(Optional)* Powered USB hub for multiple DUTs

---

### 🧠 Software (on each Raspberry Pi)
| Component | Version | Purpose |
|------------|----------|----------|
| Ubuntu Server | 24.04 LTS | Base OS |
| Python | 3.10+ | FastAPI backend |
| Docker Engine | 24.0+ | Container runtime |
| Docker Compose | v2+ | Manage container setup |
| usbip tools | latest | Share and attach USB devices |
| OpenOCD | latest | Debugging or flashing DUT |
| curl & git | latest | Testing and version control |

**Install dependencies:**
```bash
sudo apt update
sudo apt install -y python3 python3-pip docker.io docker-compose \
usbip hwdata linux-tools-$(uname -r) openocd curl git
sudo systemctl enable docker && sudo systemctl start docker
sudo usermod -aG docker $USER && newgrp docker
