from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Webhook server is running!"}

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        payload = await request.json()
        print("Received webhook payload:", payload)
        return JSONResponse(content={"message": "Webhook received!"}, status_code=200)
    except Exception as e:
        print("Error processing webhook:", str(e))
        return JSONResponse(content={"error": "Failed to process webhook"}, status_code=400)