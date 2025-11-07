FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && pip install --no-cache-dir \
        fastapi \
        uvicorn \
        python-dotenv \
        requests \
        pyyaml \
        pyserial \
        pyusb \
        loguru \
        aiofiles \
        websockets \
        psutil \
        "python-jose[cryptography]" \
        passlib \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
