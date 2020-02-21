from linebot.models import TextSendMessage, ImageSendMessage, QuickReply, QuickReplyButton, MessageAction
import random


class Reply:
    def __init__(self, event, line_bot_api):
        """ 初期化しておかないと動作不可能なクラス変数 """
        print("クラス変数初期化")
        # モードの初期化
        self.line_bot_api = line_bot_api
        # 引数として受け取ったeventをself.event変数に代入
        self.event = event
        # 受け取った場所(個チャ,グルチャ,ルームチャ)をself.type変数に代入
        self.type = event.source.type
        # 受け取った文字をtext変数へ
        self.text = event.message.text
        # user,room,groupの何れかのidによって初期値を設定
        if self.type == "user":
            self.running_id = event.source.user_id
        elif self.type == "room":
            self.running_id = event.source.room_id
        elif self.type == "group":
            self.running_id = event.source.group_id
        self.user_id = event.source.user_id
        self.display_name = line_bot_api.get_profile(self.user_id).display_name

    # モード選択メソッド
    def mode_select(self):
        # 何か言われたら、「あと返す」
        self.reply("あ")

    # リプライメソッド(送りたい文字配列)
    def reply(self, VALUES):
        for v in VALUES:
            print(f"{v}\n")
        MESSAGES = [TextSendMessage(value) for value in VALUES]
        self.line_bot_api.reply_message(self.event.reply_token, MESSAGES)
        """ 引数の数だけ返答する（公式LINEの制限によって５つまで） """
