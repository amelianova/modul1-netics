from fastapi import FastAPI
import time
import datetime
import os

start_time = time.time()
app = FastAPI()

@app.get("/health")
def health():
    uptime_seconds = int(time.time() - start_time)
    return {
        "nama": "Tunas Bimatara Chrisnanta Budiman",
        "nrp": "5025231999",
        "status": "UP",
        "timestamp": datetime.datetime.now().isoformat(),
        "uptime": f"{uptime_seconds} seconds"
    }
