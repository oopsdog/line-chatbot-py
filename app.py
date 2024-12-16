from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent
from linebot.models import TextMessage, TextSendMessage
import os
#import json
from openai import OpenAI
#import openai

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
    if ai_msg == '24hr':
        qmsg = 'Read the link https://github.com/oopsdog/line-chatbot-py/blob/main/flood_grading_by_time.csv\n'
        qmsg = qmsg + 'the column 1 is the time different comparing now. the column 2 is the water depth in cm.\n'
        qmsg = qmsg + 'if the flood water depth is greater than 30, then it is a red flag, please reply the warning to the receiver.\n'
        qmsg = qmsg + 'if the flood water depth is greater than 3 and not greater than 30, then it is a yellow flag. please remind the receiver about the remaining water.\n'
        qmsg = qmsg + 'if the flood water depth is not greater than 3 then it is a green flag. please tell the receiver it is safe.\n'

        client = OpenAI(
            organization=opai_org,
            project=opai_proj,
            api_key=opai_sect,
        )
        response = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": qmsg,
            }],
            model="gpt-4o-mini",
            #model="gpt-3.5-turbo",   
        )
        reply_msg = response.choices[0].message.content
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ai_msg))




if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)