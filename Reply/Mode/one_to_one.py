import pandas as pd


def run(self):
    self.RUNNING_ID_DICT[self.running_id].setdefault(
        "登録言葉モード", {"ステップ": "未選択", "受信登録": "未選択", "送信登録": "未選択"}
    )
    # Excelファイルを読み込む
    WORDS_DICT = {}
    sheet = pd.read_excel(
        "Reply/mode/one_to_one.xlsx", sheet_name="one_to_one", index_col=False)
    # 辞書へ追加
    for row in sheet.values:
        WORDS_DICT[row[0]] = [row[1], row[2], row[3]]
    # 現在登録済みの言葉一覧
    words_list = ""
    for word in list(WORDS_DICT):
        words_list += f"「{word}」\n"

    if self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] == "未選択":
        if self.text == "登録":
            # 登録する処理に移行
            self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] = '受信登録'
            self.reply([
                "受信する言葉を入力してください。"
            ])
        elif self.text in list(WORDS_DICT):
            # 登録済みの言葉が来たら予め登録済みの言葉を返す。
            self.reply([WORDS_DICT[self.text][0]])
        else:
            self.reply([
                "その言葉への対応は未登録です。",
                "現在登録されている言葉の一覧\n"
                + f"{words_list}です。"
                "是非とも登録してみてください！",
                "登録する場合、\n"
                + "「登録」と入力してね！！"
            ])

    elif self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] == '受信登録':
        if self.text == "辞める":
            cancel(self)
        elif self.text in list(WORDS_DICT):
            self.reply([
                "その言葉はへの対応は登録済みです。",
                "他の言葉を選択してください。",
                "現在登録されている言葉の一覧\n"
                + f"{words_list}",
                "登録を辞める場合は\n"
                + "「辞める」と入力してください。"
            ])
        else:
            self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['受信登録'] = self.text
            self.reply([f"「{self.text}」に対応する言葉を入力してください。"])
            self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] = '送信登録'

    elif self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] == '送信登録':
        self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['送信登録'] = self.text
        self.reply([
            f"「{self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['受信登録']}」\n"
            + "に対して\n"
            + f"「{self.text}」\n"
            + "を返す。",
            "上記の内容でよろしいですか？\n"
            + "「はい」\n"
            + "「いいえ」"
        ])
        self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] = '最終判断'
    elif self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] == '最終判断':
        if self.text == "はい":
            # Excelに書き込むメソッド呼び出し
            self.reply([
                f"「{self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['受信登録']}」\n"
                + "に対して\n"
                + f"「{self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['送信登録']}」\n"
                + "を登録しました。",
            ])
            register_word(self, WORDS_DICT)
        elif self.text == "いいえ":
            self.reply([
                "どこからやりなおしますか？\n"
                + "「1」受信するメッセージ\n"
                + "「2」送信するメッセージ\n"
                + "「3」やっぱり登録する\n"
                + "「4」やっぱり登録することを辞める"
            ])
            self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] = "やり直し"
        else:
            self.reply([
                f"「{self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['受信登録']}」\n"
                + "に対して\n"
                + f"「{self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['送信登録']}」\n"
                + "を返す。",
                "上記の内容でよろしいですか？\n"
                + "「はい」\n"
                + "「いいえ」"
            ])
    elif self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] == "やり直し":
        if self.text == "1":
            self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] = '受信登録'
            self.reply([
                "受信する言葉を入力してください。"
            ])
        elif self.text == "2":
            self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] = '送信登録'
            self.reply([
                f"「{self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['受信登録']}」に対応する言葉を入力してください。"
            ])
        elif self.text == "3":
            self.reply([
                f"「{self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['受信登録']}」\n"
                + "に対して\n"
                + f"「{self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['送信登録']}」\n",
                "上記の内容をやっぱり登録しておきました。"
            ])
            register_word(self, WORDS_DICT)
        elif self.text == "4":
            # 登録を辞める
            cancel(self)


def register_word(self, WORDS_DICT):
    ADD_DICT = {
        f"{self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['受信登録']}":
        [
            f"{self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['送信登録']}",
            self.user_id,
            self.display_name
        ]
    }
    WORDS_DICT.update(ADD_DICT)
    a_list = []
    for val in WORDS_DICT:
        a_list.append([
            val,
            WORDS_DICT[val][0],
            WORDS_DICT[val][1],
            WORDS_DICT[val][2]
        ])
    df = pd.DataFrame(
        a_list, columns=["受信", "送信", "ID", "LINE名"]
    )
    df.to_excel("Reply/mode/one_to_one.xlsx",
                sheet_name="one_to_one", index=False)
    print(df)
    self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] = "未選択"


def cancel(self):
    self.reply([
        "登録することを辞めました。",
        "再度登録したくなった場合は\n"
        + "「登録」と入力してください。",
        "登録言葉モードを終了したい場合は、\n"
        + "「登録言葉モード終了」と入力してください。"
    ])
    self.RUNNING_ID_DICT[self.running_id]['登録言葉モード']['ステップ'] = "未選択"
