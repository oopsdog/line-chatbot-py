from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent
from linebot.models import TextMessage, TextSendMessage
import os
#import json
from openai import OpenAI

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))
opai_sect = os.environ.get('OPEN_AI_SECRET')
opai_proj = os.environ.get('OPEN_AI_PROJECT')
opai_org = os.environ.get('OPEN_AI_ORG')


##openai.api_key = os.environ.get('OPEN_AI_SECRET')
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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message1 = event.message.text
    ai_msg = message1
    reply_msg = ''
    client = OpenAI(
        organization=opai_org,
        project=opai_proj,
        api_key=opai_sect,
    )
            # 將第六個字元之後的訊息發送給 OpenAI
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": ai_msg,
        }],
        model="gpt-4o-mini",
        #model="gpt-3.5-turbo",   
    )
            reply_msg = response.choices[0].message.content

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))





if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)