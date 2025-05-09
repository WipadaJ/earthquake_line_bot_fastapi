from fastapi import FastAPI, Request
from fastapi.responses import Response
from linebot import LineBotApi, WebhookHandler,get_subscribers
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

from fetch_earthquake import fetch_earthquake_data  # หรือใช้ fetch_earthquake_asia
from line_bot import handler  # ใช้ handler เดิมจาก line_bot.py

app = FastAPI()

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# ✅ Webhook สำหรับ LINE
@app.post("/callback")
async def callback(request: Request):
    body = await request.body()
    signature = request.headers.get('X-Line-Signature')

    print("📩 ได้รับ webhook แล้ว:", body.decode())

    try:
        handler.handle(body.decode(), signature)
        print("✅ Handler ได้รับ event แล้ว")
    except Exception as e:
        print("❌ ERROR ใน handler.handle():", e)

    return Response(content="OK", status_code=200)

# ✅ Manual push message (เช่นเรียกจากเบราว์เซอร์หรือ scheduler)
@app.get("/notify")
def manual_notify_all():
    message = fetch_earthquake_data()
    if not message or not message.strip():
        return {"status": "no data"}

    subscribers = get_subscribers()
    success = 0

    for user_id in subscribers:
        try:
            line_bot_api.push_message(user_id, TextSendMessage(text=message))
            success += 1
        except Exception as e:
            print(f"❌ Failed to push to {user_id}: {e}")

    return {"status": "sent", "users": success}

