import os
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from fetch_earthquake import fetch_earthquake_data
from config import settings
from db_connect import is_subscribed_pg, new_user_pg, terminate_user_pg, check_db_connection

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

def is_subscribed(user_id: str, filename="subscribers.txt") -> bool:
    try:
        with open(filename, "r") as f:
            for line in f:
                if line.strip() == user_id:
                    return True
        return False
    except FileNotFoundError:
        return False

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

#if __name__ == "__main__":
#    push_earthquake_alert()

def handle_line_webhook(body, signature):
    from fastapi.responses import Response
    try:
        handler.handle(body.decode(), signature)
        print("✅ Handler ได้รับ event แล้ว")
    except Exception as e:
        print("❌ ERROR ใน handler.handle() line_bot :", e)
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
                TextSendMessage(text="ขณะนี้ยังไม่มีรายงานแผ่นดินไหวในทวีปเอเชียที่มีความแรงเกิน 1.0 ค่ะ")
            )

    elif text == "สมัคร":
        if is_subscribed_pg(user_id):
            reply = "คุณเคยสมัครรับแจ้งเตือนแผ่นดินไหวแล้ว"
        else:
            new_user_pg(user_id)
            reply = "คุณได้สมัครรับแจ้งเตือนแผ่นดินไหวเรียบร้อยแล้ว!"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    elif text == "ยกเลิก":
        if is_subscribed_pg(user_id):
            terminate_user_pg(user_id)
            reply = "คุณได้ ยกเลิก รับแจ้งเตือนแผ่นดินไหวเรียบร้อยแล้ว!"
        else:
            reply = "คุณยังไม่ได้ สมัคร รับแจ้งเตือนแผ่นดินไหว"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    elif text == "รำคาน" or text == "รำคาญ":
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="ขออภัยค่ะ ดิฉันเพียงแค่ทำตามหน้าที่เท่านั้น")
            )
