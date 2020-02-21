def run(self):
    # ゲームモードが初回起動時のみ初期値を設定
    print(self.RUNNING_ID_DICT)
    now_game = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ゲームの種類"]
    print(now_game)
    # ゲーム中の場合
    if self.text in list(self.GAME_DICT)[1::] and self.mode != "未選択":
        self.reply([
            f"現在「{now_game}」をやっている最中です。",
            f"ゲームを切り替えたい場合は、「{now_game}終了」と入力後、再度他のゲームを選択してください。"
        ])
    elif self.text in self.FIN_WORDS + [f"{now_game}終了"] and self.mode != "未選択":
        self.finish()
    else:
        self.jump()


def cannot_play(self, num, ADD_TEXT):
    if self.type == "user":
        now_game = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ゲームの種類"]
        self.reply(
            [
                "おっと、やろうと思ったけどここ個チャじゃん。",
                "ここじゃこのゲームはできないぜ。"
            ]
            + ADD_TEXT
            + [
                f"このアカウントを含めた{num}人以上のグループを作ってプレイしてみてくれよな！",
                f"{now_game}を終了します。"
            ]
        )
        self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ゲームの種類"] = "未選択"
        return True
