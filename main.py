from fastapi import FastAPI, Request
from fastapi.responses import Response
from linebot import LineBotApi, WebhookHandler
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

# 🔧 โหลดรายชื่อผู้สมัครรับแจ้งเตือน
def get_subscribers():
    filename = "subscribers.txt"
    default_user = os.getenv("DEFAULT_USER_ID") or "U066bed9e80abfb1930bbca1512ec4b55"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            #pass  # สร้างไฟล์เปล่า
            f.write(default_user + "\n")
        print(f"📄 สร้าง {filename} พร้อม user id เริ่มต้นแล้ว")

    with open(filename, "r") as f:
        return list(set(line.strip() for line in f if line.strip()))

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

