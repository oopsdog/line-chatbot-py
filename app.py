from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent
from linebot.models import TextMessage, TextSendMessage
import re
#import schedule
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
#user_id = line_bot_api.get_profile('<user_id>')


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
    if ai_msg.startswith('24hr'):
    #    qmsg = 'Read the link https://github.com/oopsdog/line-chatbot-py/blob/main/flood_grading_by_time.csv\n'
        #qmsg = user_id
        qmsg = 'Read the conditions time(before)=floodmark(no flooding), time(now)=floodmark(30cm flooding),time(after)=floodmark(slight flooding)\n'
        qmsg = qmsg + 'The item 1 is the time 6 hr before now, now, and 6 hr after now. And the item2 is the flood condition.\n'
        qmsg = qmsg + 'Generate the flood warning for now and later and reminder in 150 words.\n'

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

    elif ai_msg.startswith('COND'):
        match = re.search(r"COND([A-Z]{3})", text)
        bef = match.group(1)
        now = match.group(2)
        aft = match.group(3)
        test_msg = bef + now + aft + " test test"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=test_msg))
    elif ai_msg.startswith('Hi'):
        client = OpenAI(
            organization=opai_org,
            project=opai_proj,
            api_key=opai_sect,
        )
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
    elif ai_msg.startswith('flood here'):
        reply_msg = 'https://github.com/oopsdog/line-chatbot-py/blob/main/flood_contour_map.png'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))
    elif ai_msg.startswith('check'):
        file_path = os.path.join(os.getcwd(), '.', 'test.txt')
        with open(file_path, 'r') as file:
            content = file.read()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ai_msg))


#
# Schedule the message to run automatically
# schedule.every(10).seconds.do(push_message)  # Auto-push every 10 seconds for demonstration


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)