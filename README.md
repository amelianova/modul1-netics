FastAPI Health Check - CI/CD Deployment
=======================================

Repositori ini merupakan implementasi dari modul CI/CD dalam bentuk API sederhana dengan endpoint `/health`. Proyek ini dibuat menggunakan FastAPI dan dideploy menggunakan Docker multi-stage ke sebuah VPS publik. Proses deployment diotomasi melalui GitHub Actions.

Identitas
---------
- Nama: Amelia Nova Safitri
- NRP: 5025231041

Tujuan Pengerjaan
-----------------
Membuat API `/health` yang menampilkan status server serta menerapkan CI/CD dengan GitHub Actions untuk proses otomatisasi deploy ke server berbasis container.

Teknologi yang Digunakan
-------------------------
- Bahasa: Python (FastAPI)
- Web server: Uvicorn
- Containerization: Docker
- CI/CD: GitHub Actions
- Hosting: VPS Ubuntu 22.04
- Sistem Operasi Lokal: Windows 10 (dengan WSL/Git Bash)

Endpoint /health
----------------
Endpoint ini akan menampilkan informasi status API dan uptime server. Contoh response:
```
{
  "nama": "Tunas Bimatara Chrisnanta Budiman",
  "nrp": "5025231999",
  "status": "UP",
  "timestamp": "2025-04-06T10:20:45.123Z",
  "uptime": 125.23
}
```

Struktur File
-------------
```
fastapi-health/
├── .github/
│   └── workflows/
│       └── deploy.yml         # CI/CD workflow
├── Dockerfile                 # Multi-stage build
├── main.py                   # FastAPI source
├── requirements.txt          # Python dependencies
├── README.md                 # Dokumentasi ini
```

Langkah Pengerjaan
------------------

1. Membuat API FastAPI

File main.py:
```
from fastapi import FastAPI
from datetime import datetime
import time

app = FastAPI()
start_time = time.time()

@app.get("/health")
def health_check():
    current_time = datetime.utcnow().isoformat()
    uptime = round(time.time() - start_time, 2)

    return {
        "nama": "Tunas Bimatara Chrisnanta Budiman",
        "nrp": "5025231999",
        "status": "UP",
        "timestamp": current_time,
        "uptime": uptime
    }
```

2. Menulis requirements.txt
```
fastapi
uvicorn
```

3. Menulis Dockerfile (Multi-stage Build)
```
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY main.py .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

4. Menyiapkan Server VPS
- OS: Ubuntu 22.04
- Gunakan azure.com untuk memperoleh vps secara gratis
- Buat user `amel`
  sumber: https://youtu.be/4xGPfVfJ4iM?si=YlIX4V3L-p3dCWfk


5. Setup SSH Key & GitHub
- Buat SSH key di lokal (ssh-keygen)
- Tambahkan ke GitHub (Settings → SSH and GPG keys)
- Tambahkan public key GitHub ke VPS (~/.ssh/authorized_keys)
- Tambahkan VPS IP ke known hosts:
  ssh-keyscan -H <ip-vps> >> ~/.ssh/known_hosts

6. Setup CI/CD: deploy.yml
```
.github/workflows/deploy.yml:

name: CI/CD FastAPI

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Deploy to VPS
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_KEY }}
        script: |
          cd ~/fastapi-health || git clone https://github.com/amelianova/modul1-netics.git fastapi-health && cd fastapi-health
          git pull origin main
          docker stop fastapi-health || true && docker rm fastapi-health || true
          docker rmi fastapi-health || true
          docker build -t fastapi-health .
          docker run -d -p 80:8000 --name fastapi-health fastapi-health
```
Note: Tambahkan SERVER_HOST, SERVER_USER, dan SERVER_KEY ke GitHub Secrets.

Hasil Akhir
-----------
API berhasil:
- Diakses via curl http://20.2.64.250/health
- Diakses dari browser http://20.2.64.250/health
- Dideploy otomatis ketika push ke branch main

Catatan Tambahan
----------------
- Uvicorn berjalan di dalam container pada port 8000 dan di-expose ke port 80 VPS
- Docker digunakan dengan pendekatan multi-stage agar image lebih ringan
- CI/CD menggunakan best practice: memisahkan konfigurasi via GitHub Secrets dan menggunakan action yang aman (appleboy/ssh-action)

