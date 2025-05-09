import os
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from fetch_earthquake import fetch_earthquake_data

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
def get_subscribers():
    try:
        with open("subscribers.txt", "r") as f:
            return list(set(line.strip() for line in f))
    except FileNotFoundError:
        return []

def push_earthquake_alert():
    message = fetch_earthquake_data()  # หรือ fetch เฉพาะ event ใหม่
    if not message:
        print("❌ ไม่มีข้อมูลแผ่นดินไหวใหม่")
        return

    for user_id in get_subscribers():
        try:
            line_bot_api.push_message(user_id, TextSendMessage(text=message))
            print("✅ ส่งแจ้งเตือนให้:", user_id)
        except Exception as e:
            print("❌ ส่งไม่สำเร็จ:", e)

if __name__ == "__main__":
    push_earthquake_alert()

# def handle_line_webhook(body, signature):
#     from fastapi.responses import Response
#     try:
#         handler.handle(body.decode(), signature)
#         print("✅ Handler ได้รับ event แล้ว")
#     except Exception as e:
#         print("❌ ERROR ใน handler.handle():", e)
#     return Response(content="OK", status_code=200)

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     user_id = event.source.user_id
#     text = event.message.text.strip()
    
#     if text == "แผ่นดินไหวล่าสุด":
#         info = fetch_earthquake_data()
#         print("🔎 DEBUG info = ", repr(info))  # สำคัญมาก

#         if info and info.strip():
#             line_bot_api.reply_message(
#                 event.reply_token,
#                 TextSendMessage(text=info)
#             )
#         else:
#             line_bot_api.reply_message(
#                 event.reply_token,
#                 TextSendMessage(text="ขณะนี้ยังไม่มีรายงานแผ่นดินไหวในทวีปเอเชียที่มีความแรงเกิน 1.0 ค่ะ")
#             )

#     elif text == "สมัคร":
#         user_id = event.source.user_id
#         with open("subscribers.txt", "a") as f:
#             f.write(user_id + "\n")

#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text="คุณได้สมัครรับแจ้งเตือนแผ่นดินไหวเรียบร้อยแล้ว!")
#         )
