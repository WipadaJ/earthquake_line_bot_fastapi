import os
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

def handle_line_webhook(body, signature):
    from fastapi.responses import Response
    try:
        handler.handle(body.decode(), signature)
    except Exception as e:
        print("Error:", e)
    return Response(content="OK", status_code=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    
    if text == "สมัคร":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="คุณได้สมัครรับแจ้งเตือนแผ่นดินไหวเรียบร้อยแล้ว!")
        )