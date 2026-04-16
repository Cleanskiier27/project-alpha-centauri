from fastapi import FastAPI
import uvicorn
import time

app = FastAPI(title="Aerospace Mission Host", version="1.0.0")

@app.get("/")
def read_root():
    return {
        "status": "AEROSPACE_HOST_ONLINE",
        "orbital_sync": "ESTABLISHED",
        "telemetry_stream": "ACTIVE",
        "timestamp": time.time()
    }

@app.get("/telemetry")
def get_telemetry():
    return {
        "alt": 42000,
        "vel": 7.8, # km/s
        "fuel": "85%",
        "agent_tasks": ["ORBIT_CORRECTION", "SIGNAL_RELAY"]
    }

if __name__ == "__main__":
    print("🚀 Launching Aerospace Host Server on Port 8080...")
    uvicorn.run(app, host="127.0.0.1", port=8080)
