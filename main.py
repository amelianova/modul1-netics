from fastapi import FastAPI
from datetime import datetime
import time
import os

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
        "uptime": f"{uptime} seconds"
    }
