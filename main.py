from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json

app = FastAPI()

# ✅ Debug flag: set to True to print everything
DEBUG = True

@app.get("/")
async def root():
    return {"status": "Webhook server is running!"}

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        payload = await request.json()

        if DEBUG:
            print("\n🔍 DEBUG: Full incoming payload:")
            print(json.dumps(payload, indent=4))

        # Extract form fields safely
        fields = payload.get("fields", {})
        meta = payload.get("meta_data", {})

        return JSONResponse(content={"message": "Webhook received successfully"}, status_code=200)

    except Exception as e:
        print("❌ Error processing webhook:", str(e))
        return JSONResponse(content={"error": "Failed to process webhook"}, status_code=400)