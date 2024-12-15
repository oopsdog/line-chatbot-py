from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

line_bot_api = LineBotApi('QeMNMBwE526qcxcuI7vyoFypvubjpoUl0qg3xiGNoC3D4ZABbdc3Mqiw+WO3YQjxGEKkOKDbEkOCFz35anisP6SD6e4lfdfOqMhA700zNm/+OMIObmQwJIqNhRS1hxLT/02Q8NQwDGt1QZb1v4+7TwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('26baa5ef3667c3bf638184ccbc2af04f')

## 

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)