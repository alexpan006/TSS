import asyncio
import httpx
from fastapi import FastAPI
import uvicorn
app = FastAPI()

# List of signer URLs (adjust based on your setup)
SIGNERS = [
    "http://signer1:8000",
    "http://signer2:8000",
    "http://signer3:8000",
]

async def trigger_keygen():
    async with httpx.AsyncClient() as client:
        tasks = [client.post(f"{signer}/keygen") for signer in SIGNERS]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            if not response.is_success:
                raise Exception(f"Keygen failed for {response.url}")
        return {"status": "success", "message": "Keygen completed for all signers"}

@app.post("/start_keygen")
async def start_keygen():
    try:
        result = await trigger_keygen()
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Main function to run the coordinator
if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)