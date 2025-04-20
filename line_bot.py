import os
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from fetch_earthquake import fetch_earthquake_data

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

def handle_line_webhook(body, signature):
    from fastapi.responses import Response
    try:
        handler.handle(body.decode(), signature)
        print("✅ Handler ได้รับ event แล้ว")
    except Exception as e:
        print("❌ ERROR ใน handler.handle():", e)
    return Response(content="OK", status_code=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    
    if text == "แผ่นดินไหวล่าสุด":
        info = fetch_earthquake_data()
        print("🔎 DEBUG info = ", repr(info))  # สำคัญมาก

        if info and info.strip():
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=info)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="ขณะนี้ยังไม่มีรายงานแผ่นดินไหวล่าสุดค่ะ")
            )

    elif text == "สมัคร":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="คุณได้สมัครรับแจ้งเตือนแผ่นดินไหวเรียบร้อยแล้ว!")
        )
