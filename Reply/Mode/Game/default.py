# ゲームモードにおけるゲーム未選択時
def run(self):
    print("ゲームモード＆ゲームの種類[未選択]")
    for i, value in enumerate(list(self.GAME_DICT)[1::], 1):
        if self.text == f"{i}":
            self.text = value
        if self.text == value:
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ゲームの種類"] = value
            # 選択時のメッセージ
            self.game_msg = [
                f"「{value}」が選択されました。\n"
                + "ゲームを終了したい場合は、\n"
                + f"「{value}終了」\n"
                + "と入力してください。"
            ]
            # Excelにゲーム毎の初回起動時の文言があれば追加
            if f"{self.GAME_DICT[value][1]}" != "nan":
                print("---Excel参照---")
                for v in self.GAME_DICT[value][1].split("\n\n"):
                    print(v)
                print("---Excel参照---")
                self.game_msg += self.GAME_DICT[value][1].split("\n\n")
                # 各ゲームモードへジャンプ
            self.jump()
            return

    if self.text in ["ゲーム一覧", "ゲーム"]:
        self.reply(self.make_list("ゲーム", list(self.GAME_DICT)[1::]))
    else:
        self.reply([
            "遊びたいゲームを選択してください",
            "「ゲーム」や「ゲーム一覧」と入力するとゲームの一覧を確認する事が出来ます。",
            "ゲームをしない場合は、「ゲームモード終了」と入力してください"
        ])
