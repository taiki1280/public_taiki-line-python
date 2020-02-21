# デフォルトモード
def run(self):
    import pandas as pd
    sheet = pd.read_excel(
        "Reply/Mode/dictionary.xlsx",
        sheet_name="default",
        index_col=False,
    )
    # 辞書へ追加
    REPLY_DICT = {}
    for row in sheet.values:
        # 想定受信文字と設定済みの返答文字の辞書を作成
        REPLY_DICT[row[0]] = {
            "受信": row[1].split("\n"),
            "返答": row[2].split("\n\n")
        }
    print("通り道")
    for i, value in enumerate(list(self.MODE_DICT)[1::], 1):
        # 数値をモード名に変換
        if self.text == f"{i}":
            self.text = value
        # 受け取ったメッセージによってやることを変更
        for i, v in enumerate(list(REPLY_DICT), 1):
            if self.text in REPLY_DICT[v]["受信"]:
                self.reply(switch_by_words(self, REPLY_DICT, v, i))
                return
        # モード選択されたとき
        if self.text == value:
            self.RUNNING_ID_DICT[self.running_id]["モード"] = value
            self.value = [
                f"{value}が選択されました。\n"
                + f"「{value}終了」\n"
                + f"と入力されるまで{value}になります。"
            ]
            # モードによって文言を追加
            if value == "ゲームモード":
                self.value += self.make_list("ゲーム", list(self.GAME_DICT)[1::])
                self.RUNNING_ID_DICT[self.running_id].setdefault(
                    "ゲームモード", {"ゲームの種類": "未選択"})
                self.reply(self.value)
                return
            elif f"{self.MODE_DICT[value][1]}" != "nan":
                # Excel参照し、改行ごとにメッセージ送信用
                self.value += self.MODE_DICT[value][1].split("\n\n")
                self.reply(self.value)
                return
            else:
                self.jump()
    if self.event.source.user_id == "Uffc2e609077732c505aae085ba524938" and self.type == "user":
        from ..taiki import taiki
        taiki.run(self)
    else:
        # Excelファイルを読み込む
        WORDS_DICT = {}
        import pandas as pd
        sheet = pd.read_excel(
            "Reply/Mode/one_to_one.xlsx", sheet_name="one_to_one", index_col=False)
        # 辞書へ追加
        for row in sheet.values:
            # [想定受信文字] = {}
            WORDS_DICT[row[0]] = [row[1], row[2], row[3]]
        if self.text in list(WORDS_DICT):
            self.reply([WORDS_DICT[self.text][0]])
        else:
            self.reply([
                "This is Taiki's bot",
                "今出来ることは「コマンド」と入力すれば一覧を表示できます。"
            ])


def switch_by_words(self, REPLY_DICT, v, i):
    value = REPLY_DICT[v]["返答"]
    if i == 1:
        value = [f"「{self.text}」" + v for v in REPLY_DICT[v]["返答"]]
    elif i == 2:
        self.RUNNING_ID_DICT[self.running_id]["モード"] = "沈黙モード"
    elif i == 3:
        value = self.make_list("コマンド", list(self.MODE_DICT)[1::])
    return value
