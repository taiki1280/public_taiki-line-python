from Reply import reply
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage
import os

# flaskのwebフレームワークのクラス(Flask)のインスタンス作成
app = Flask(__name__)

# 環境変数取得
with open("token.txt", encoding="utf-8") as f:
    FILE = [f.strip("\n") for f in f.readlines()]
    YOUR_CHANNEL_ACCESS_TOKEN = FILE[1]
    YOUR_CHANNEL_SECRET = FILE[3]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# サーバーが正常に動作しているかの確認
@app.route("/")
def hello_world():
    return "hello world!"


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

# 文字を受け取った時
@handler.add(MessageEvent, message=TextMessage)
def mode_select(event):
    obj = reply.Reply(event, line_bot_api)
    obj.mode_select()
    # reply.mode_select(event)

# スタンプを受け取った時
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )


if __name__ == "__main__":
    # app.run()
    app.run(host="0.0.0.0", port=8000)
