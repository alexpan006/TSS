import subprocess
from fastapi import FastAPI, HTTPException
import os

app = FastAPI()

# Environment variables (set via docker-compose.yml or similar)
SIGNER_ID = int(os.getenv("SIGNER_ID"))
STATE_MANAGER_URL = os.getenv("STATE_MANAGER_URL", "http://coordinator:8000")
KEYS_FILE = f"keys{SIGNER_ID}.store"
THRESHOLD_PARAMS = os.getenv("THRESHOLD_PARAMS", "1/3")  # e.g., "1/3" for 2-of-3

@app.post("/keygen")
async def run_keygen():
    try:
        # Construct the keygen command
        cmd = [
            "./tss_cli", "keygen",
            "--addr", STATE_MANAGER_URL,
            KEYS_FILE,
            THRESHOLD_PARAMS
        ]
        # Run the subprocess
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Keygen failed: {result.stderr}")
        return {"status": "success", "message": f"Keygen completed for signer {SIGNER_ID}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))