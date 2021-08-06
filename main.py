from flask import Flask, request, abort
import json, requests
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent,TextMessage, TextSendMessage, StickerSendMessage, ImageSendMessage,TemplateSendMessage
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
import os

app = Flask(__name__)



line_bot_api = LineBotApi(os.environ.get('LINE_BOT_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_BOT_SECRET'))

@app.route('/')
def index():
    return "hello world"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except LineBotApiError as e:
        app.logger.exception(f'LineBotApiError: {e.status_code} {e.message}', e)
        raise e
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # lineでテキスト送信した際のイベント設定
    try:
        print(event.message.text)
        # qr or QRと送信とPASSと送信された場合のreply_messageを設定
        if event.message.text == "qr" or event.message.text == "QR":
            message="QR要求を受け取りました"
        elif event.message.text == "PASS":
            message = "PASS要求を受け取りました"
        else:
　　　　　　　# 上記以外のメッセージ要求の場合、要求した同じメッセージ内容をmessage変数に代入する
            message = event.message.text

# linebotでの返答内容をreply_messageで設定        
line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message)) 
# 例外でエラー内容を取得
    except Exception as e:
        print(e)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="取得に失敗しました。\n再度取得をお願いします。"))

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
