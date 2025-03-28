from fastapi import FastAPI
import time
import datetime

app = FastAPI()

start_time = time.time()

@app.get("/health")

def health_check():
    return {
        "nama": "Tunas Bimatara Chrisnanta Budiman",
        "nrp": "5025231999",
        "status": "UP",
        "timestamp": datetime.datetime.now().isoformat(),
        "uptime": f"{round(time.time() - start_time, 2)}s"
    }
