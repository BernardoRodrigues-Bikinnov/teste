from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
from app.parser import parse_elementor_request  # ✅ absolute import

app = FastAPI()

DEBUG = True

@app.get("/")
async def root():
    return {"status": "Webhook server is running!"}

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        # Read raw body
        raw_body = await request.body()
        body_text = raw_body.decode("utf-8")

        # Try to get form data
        try:
            form_data = await request.form()
        except Exception:
            form_data = None

        # Parse using external parser function
        cleaned_data = parse_elementor_request(body_text, form_data)

        if DEBUG:
            print("\n🧩 Cleaned & Parsed Data (JSON):")
            print(json.dumps(cleaned_data, indent=4, ensure_ascii=False))

        return JSONResponse(
            content={"message": "Webhook received successfully", "data": cleaned_data},
            status_code=200
        )

    except Exception as e:
        print(f"❌ Error processing webhook: {str(e)}")
        return JSONResponse(content={"error": "Failed to process webhook"}, status_code=400)