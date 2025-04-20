from fastapi import FastAPI, Request
from line_bot import handle_line_webhook

app = FastAPI()

@app.post("/callback")
async def callback(request: Request):
    body = await request.body()
    signature = request.headers.get('X-Line-Signature')
    print("📩 ได้รับ webhook แล้ว:", body.decode())
    return handle_line_webhook(body, signature)
