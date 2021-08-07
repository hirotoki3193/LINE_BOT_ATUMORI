from flask import Flask, request, abort
import os
import psycopg2

from psycopg2.extras import DictCursor

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_BOT_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.environ.get("LINE_BOT_SECRET")
DATABASE_URL = os.environ.get('DATABASE_URL')

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def get_response_message(mes_from):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM pokemon_status WHERE name02='{}'".format(mes_from))
            rows = cur.fetchall()
            return rows
        

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    rows = get_response_message(event.message.text)
    
    if len(rows)==0:
         line_bot_api.reply_message(
             event.reply_token,
             TextSendMessage(text='分かりません...'))
    else:
        r = rows[0]
        reply_message = f'{r[1]}の情報は...\n'\
                        f'価格:{r[3]}\n'\
                        f'場所は{r[4]}\n'\
                        f'魚影の大きさは{r[2]}'

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
