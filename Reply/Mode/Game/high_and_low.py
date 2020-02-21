import random


def run(self):
    if "ハイアンドロー" not in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]:
        # 初回のご利用
        self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ハイアンドロー"] = {
            "自分の答え": 0,
            "CPUの答え": 0,
            "ミス回数": 1,
            "ステップ": 1
        }
        self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ハイアンドロー"]["自分の答え"] = \
            random.randrange(1, 14)
        self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ハイアンドロー"]["CPUの答え"] = \
            random.randrange(1, 14)
        self.reply(
            self.game_msg
            + [
                "私が持っている数値は"
                + f"「{self.RUNNING_ID_DICT[self.running_id]['ゲームモード']['ハイアンドロー']['CPUの答え']}」です。"
            ]
        )
        return
    my_num = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ハイアンドロー"]["自分の答え"]
    cpu_num = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ハイアンドロー"]["CPUの答え"]
    if self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ハイアンドロー"]["ステップ"] == 1:
        # 二回目以降のご利用
        high = ["上", "うえ", "はい", "ハイ", "High", "high"]
        low = ["下", "した", "ろー", "ロー", "Low", "low"]
        if self.text in high or self.text in low:
            if cpu_num == my_num:
                judge(self, "引き分け")
            elif cpu_num < my_num and self.text in high or cpu_num > my_num and self.text in low:
                judge(self, "あなたの勝ち")
            else:
                judge(self, "あなたの負け")
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ハイアンドロー"]["ステップ"] = 2
            # 値を変更
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ハイアンドロー"]["自分の答え"] = \
                random.randrange(1, 14)
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ハイアンドロー"]["CPUの答え"] = \
                cpu_num = random.randrange(1, 14)
        else:
            self.reply(["HighかLowを表す言葉を入力してください。"])
        # コンティニュー？
    elif self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ハイアンドロー"]["ステップ"] == 2:
        if self.text in ["はい", "うん", "Yes", "yes", "YES"]:
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ハイアンドロー"]["ステップ"] = 1
            self.reply([f"相手の数値は「{cpu_num}」です。"])
        elif self.text in ["いいえ", "ううん", "No", "no", "NO"]:
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"].pop("ゲームの種類")
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["ゲームの種類"] = "未選択"
            self.reply(["ハイアンドローを終了します。"])
        else:
            self.reply(["Continue...？\n「Yes」\n「No」"])


def judge(self, result):
    self.reply([
        f"{result}です。",
        f"只今の貴方の数値は「{self.RUNNING_ID_DICT[self.running_id]['ゲームモード']['ハイアンドロー']['自分の答え']}」でした。",
        "ゲームを続けますか？\n"
        + "「はい」\n"
        + "「いいえ」"
    ])
