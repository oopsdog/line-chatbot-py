from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent
from linebot.models import TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv['CHANNEL_ACCESS_TOKEN'], None)
handler = WebhookHandler(os.getenv['CHANNEL_SECRET'], None)
##parser = WebhookParser(os.environ['CHANNEL_SECRET'])

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

##@handler.add(MessageEvent, message=TextMessage)
##def handle_message(event):
##    message1 = event.message.text
##    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message1))

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):

    # 當 LINE 後台發送測試訊號過來時，會使用一組假 token，無視它就好
    if event.reply_token == '0' * 32:
        return

    # 暫停 1.5 秒，假裝在打字或讀訊息
    time.sleep(1.5)

    # 隨機回覆一串敷衍訊息
    linebot_client.reply_message(
        event.reply_token,
        TextSendMessage(
            random.choice([
                '好',
                'ok',
                '恩～',
                '我知道了',
            ])
        )
    )


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)