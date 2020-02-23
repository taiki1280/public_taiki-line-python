from linebot.models import TextSendMessage, ImageSendMessage, QuickReply, QuickReplyButton, MessageAction
import random


class Reply:
    # 全クラスで使用する為のクラス変数
    print("クラス辞書初期化")
    RUNNING_ID_DICT = {}
    MODE_DICT = {}
    HIDDEN_MODE_DICT = {}
    GAME_DICT = {}

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
        # MODE_DICTへExcelから読み込む
        self.sheet_to_dict("mode", self.MODE_DICT)
        # MODE_DICTへExcelから読み込む
        self.sheet_to_dict("hidden_mode", self.HIDDEN_MODE_DICT)
        # GAME_DICTへExcelから読み込む
        self.sheet_to_dict("game", self.GAME_DICT)
        # botが使われている場所を一意に特定したIDで、辞書を作成
        self.RUNNING_ID_DICT.setdefault(self.running_id, {"モード": "未選択"})
        self.FIN_WORDS = ["fin", "Fin", "FIN",
                          "exit", "Exit", "EXIT" "おわり", "終了"]

    # モード選択メソッド
    def mode_select(self):
        print("mode_select起動")
        self.mode = self.RUNNING_ID_DICT[self.running_id]["モード"]
        """ モードに関わらず条件によって実行される処理 """
        if self.text in ["Command", "command"]:
            self.reply(self.make_list("コマンド", list(self.MODE_DICT)[1::]))
        elif self.text in ["@bye", "退会願います", "帰れ", "去れ"]:
            self.leave()
        elif self.text in list(self.MODE_DICT)[1::] and self.mode != "未選択":
            self.selected_same(self.mode, "モード")
        elif self.text in self.FIN_WORDS + [f"{self.mode}終了"] and self.mode != "未選択":
            self.finish()
        else:
            self.jump()

    # Excelのシート名を辞書に登録するメソッド。引数(シート名,辞書名)
    def sheet_to_dict(self, value, dic_name):
        import pandas as pd
        sheet = pd.read_excel("Reply/Mode/dictionary.xlsx", sheet_name=value)
        for row in sheet.values:
            dic_name[row[0]] = row[1], row[2]

    # 一覧作成メソッド（コマンド、ゲーム選択など)
    def make_list(self, kind, VALUE_LIST):
        print("一覧作成メソッド")
        made_list = ""
        for i, value in enumerate(VALUE_LIST, 1):
            made_list += f"\n{i:02}. 「{value}」"
        return [
            f"現在使用可能な{kind}は{i}個です。",
            f"「{kind}一覧」\n"
            + f"{made_list}",
            "日本語のみを入力してください。",
            f"例）{VALUE_LIST[random.randrange(i)]}"
        ]

    # モード選択済みの時にモード選択された時
    def selected_same(self, value, something):
        print("モード選択済み")
        self.reply([
            f"今既に{value}やで...？",
            f"「{value}終了」といわれるまで「{value}」になります",
            f"他の{something}に切り替えたい場合は現在の{something}を終了してください。"
        ])

    # 終了メソッド
    def finish(self):
        print("終了メソッド")
        fin_value, kind, VALUE_DICT = self.mode, "コマンド", self.MODE_DICT
        if self.mode == "ゲームモード":
            now_game = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ゲームの種類"]
            if now_game != "未選択":
                self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ゲームの種類"] = "未選択"
                fin_value, kind, VALUE_DICT = now_game, "ゲーム", self.GAME_DICT
            else:
                self.RUNNING_ID_DICT[self.running_id]["モード"] = "未選択"
        else:
            if self.mode == "財布モード":
                self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ステップ"] = 0
            elif self.mode in self.RUNNING_ID_DICT[self.running_id]:
                del(self.RUNNING_ID_DICT[self.running_id][self.mode])
            self.RUNNING_ID_DICT[self.running_id]["モード"] = "未選択"
        self.reply(
            [
                f"「{fin_value}」を終了しました。\n"
                + f"下記の一覧から{kind}を入力してください。"
            ]
            + self.make_list(kind, list(VALUE_DICT)[1::])
        )

    # 選択されたモードへ飛ぶメソッド
    def jump(self):
        print("ジャンプメソッド")
        value = self.RUNNING_ID_DICT[self.running_id]["モード"]
        game = ""
        if self.mode == "ゲームモード":
            value = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ゲームの種類"]
            # value = "未選択"
            game = ".Game"
            VALUE_DICT = self.GAME_DICT
        elif value in self.MODE_DICT:
            VALUE_DICT = self.MODE_DICT
        # インポートがある場合はインポート
        if f"{VALUE_DICT[value][0]}" != "nan":
            exec(f"from Reply.Mode{game} import {VALUE_DICT[value][0]}")
        # メソッド呼び出し
        exec(f"{VALUE_DICT[value][0]}.run(self)")

    # リプライメソッド(送りたい文字配列)
    def reply(self, VALUES):
        for v in VALUES:
            print(f"{v}\n")
        MESSAGES = [TextSendMessage(value) for value in VALUES]
        self.line_bot_api.reply_message(self.event.reply_token, MESSAGES)
        """ 引数の数だけ返答する（公式LINEの制限によって５つまで） """

    def reply_img(self, file_id):
        ImageSendMessage()
        messages = ImageSendMessage(

            original_content_url=f"https://drive.google.com/uc?id={file_id}",
            preview_image_url=f"https://drive.google.com/uc?id={file_id}"
        )
        self.line_bot_api.reply_message(self.event.reply_token, messages)

    # クイックリプライメソッド(送りたい文字列,ボタンの文字列)
    def quick_reply(self, VALUES, BUTTONS):
        print("クイックリプライメソッド")
        # (ボタン、送信文字列）
        items = [QuickReplyButton(None, MessageAction(l, l)) for l in BUTTONS]
        # items = [
        #     QuickReplyButton(None, MessageAction(l, t)) for l, t in zip(BUTTONS, BUTTONS)
        # ]
        MESSAGES = [TextSendMessage(v, QuickReply(items)) for v in VALUES]
        self.line_bot_api.reply_message(self.event.reply_token, MESSAGES)
        """ リストの数は13個まで（公式LINEの制限によって5つまで） """

    # プッシュメソッド
    def push(self, VALUES, user_id):
        print("プッシュメソッド")
        MESSAGES = [TextSendMessage(text=v) for v in VALUES]
        self.line_bot_api.push_message(user_id, MESSAGES)

    # 退会メソッド
    def leave(self):
        print("退会メソッド")
        # グループ又はルームチャットの時
        if self.type in "user":
            self.reply(["個人チャットなので、退会処理は出来兼ねます。"])
            return
        else:
            self.reply(["分かりました。", "退会します。"])
            exec(f"self.line_bot_api.leave_{self.type}(self.running_id)")
            del(self.RUNNING_ID_DICT[self.running_id])
