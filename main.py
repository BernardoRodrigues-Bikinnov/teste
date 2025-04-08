from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json

app = FastAPI()

DEBUG = True


@app.get("/")
async def root():
    return {"status": "Webhook server is running!"}


def clean_field_name(raw_key):
    # Remove "fields[" and "]" from Elementor field keys
    if raw_key.startswith("fields[") and raw_key.endswith("]"):
        return raw_key[len("fields["):-1]
    return raw_key


@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        # Get raw body
        raw_body = await request.body()
        body_text = raw_body.decode("utf-8")

        if DEBUG:
            print("\n🔍 DEBUG: Raw body text received:")
            print(body_text)

        # Try parsing as JSON
        try:
            payload = json.loads(body_text)
            if DEBUG:
                print("\n🔍 DEBUG: Parsed JSON payload:")
                print(json.dumps(payload, indent=4))

            fields = payload.get("fields", {})
            meta = payload.get("meta_data", {})

            print("\n📥 Form fields received:")
            for field_name, field_value in fields.items():
                print(f"- {field_name}: {field_value}")

            print("\nℹ️ Meta data:")
            for meta_name, meta_value in meta.items():
                print(f"- {meta_name}: {meta_value}")

        except json.JSONDecodeError:
            # Fallback: handle form data dynamically
            form_data = await request.form()
            print("\n📥 Form data received:")
            cleaned_data = {}
            for raw_key, value in form_data.items():
                clean_key = clean_field_name(raw_key)
                cleaned_data[clean_key] = value
                print(f"- {clean_key}: {value}")

        return JSONResponse(content={"message": "Webhook received successfully"}, status_code=200)

    except Exception as e:
        print("❌ Error processing webhook:", str(e))
        return JSONResponse(content={"error": "Failed to process webhook"}, status_code=400)