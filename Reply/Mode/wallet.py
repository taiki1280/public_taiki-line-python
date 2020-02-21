import random


# 財布モード
def run(self):
    if "財布モード" not in self.RUNNING_ID_DICT[self.running_id]:
        self.RUNNING_ID_DICT[self.running_id]["財布モード"] = {
            "入力値": 0, "現在の所持金": 0, "ミス回数": 1, "ステップ": 1
        }
        self.reply([
            "財布の中身を記録しておくために数値を保持するだけのモードです。",
            "なお現在開発中の為、値の保持がしばしば出来なくなると思います。\n"
            + "ご了承ください。"
            "そうなった際にはお手数ですがトーク履歴より値を再入力してください。",
            "あなたの所持金を入力してください。",
            "例）「0」"
        ])
        return
    money = self.RUNNING_ID_DICT[self.running_id]["財布モード"]["入力値"]
    if self.text in ["リセット", "Reset", "削除", "リスタート", "Delete"]:
        del(self.RUNNING_ID_DICT[self.running_id]["財布モード"])
        self.reply(
            [
                "データを全削除しました。\n"
                + "財布モードを終了しました。"
            ]
            + self.make_list("コマンド", list(self.MODE_DICT))
        )
        self.RUNNING_ID_DICT[self.running_id]["モード"] = "未選択"
        return
    elif self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ステップ"] == 0:
        self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ステップ"] = 1
        self.reply([
            "前回までの所持金は\n"
            + f"「{self.RUNNING_ID_DICT[self.running_id]['財布モード']['現在の所持金']}円」です。\n"
            + "値に変更がある場合は\n"
            + "「整数」を入力後、「たす」或いは「ひく」を入力してください。",
            "特に変更がなければ「財布モード終了」と入力してください。"
        ])
        return
    elif self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ステップ"] == 1:
        if self.text.isdigit():
            self.RUNNING_ID_DICT[self.running_id]["財布モード"]["入力値"] = int(
                self.text)
            if self.RUNNING_ID_DICT[self.running_id]["財布モード"]["入力値"] == 0:
                if self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ミス回数"] == 1:
                    self.reply([
                        "流石にそれは無いやろww",
                        "どうやって生活してるんですか...？",
                        "あなたにとってこのモードの利用価値はありますか？？"
                    ])
                elif self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ミス回数"] == 2:
                    self.reply(["え、本当に...？", "まじで...？"])
                elif self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ミス回数"] == 3:
                    self.reply(["次はないからな？？", "それでいいんだな？？"])
                else:
                    self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ミス回数"] += 1
            else:
                self.RUNNING_ID_DICT[self.running_id]["財布モード"]["現在の所持金"] = int(
                    self.text)
                self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ステップ"] = 2
                self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ミス回数"] = 1
                self.reply([
                    "現在の所持金を",
                    f"「{self.RUNNING_ID_DICT[self.running_id]['財布モード']['現在の所持金']}円」",
                    "にセットしました。",
                    "値に変更がある場合は\n"
                    + "「整数」を入力後\n"
                    + "「たす」或いは「ひく」を入力してください。",
                    "特に変更がなければ「財布モード終了」と入力してください"
                ])
                return
        else:
            self.reply([
                "現在の所持金は\n"
                + f"「{self.RUNNING_ID_DICT[self.running_id]['財布モード']['現在の所持金']}円」です。",
                "値に変更がある場合は\n"
                + "「整数」を入力後\n"
                + "「たす」或いは「ひく」を入力してください。",
                "特に変更がなければ、\n"
                + "「財布モード終了」\n"
                + "と入力してください。"
            ])
    elif self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ステップ"] == 2:
        if self.text.isdigit():
            self.RUNNING_ID_DICT[self.running_id]["財布モード"]["入力値"] = int(
                self.text)
            if self.RUNNING_ID_DICT[self.running_id]["財布モード"]["入力値"] != 0:
                self.reply([
                    "「たす」或いは「ひく」を入力してください。",
                    "やっぱり変更がなければ「財布モード終了」と入力してください"
                ])
                self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ステップ"] = 3
                return
            else:
                self.reply(["変更ないやんww", "出直しなw"])
        else:
            self.reply([
                "現在の所持金は\n"
                + f"「{self.RUNNING_ID_DICT[self.running_id]['財布モード']['現在の所持金']}円」です。",
                "値に変更がある場合は\n"
                + "「整数」を入力後\n"
                + "「たす」或いは「ひく」を入力してください。",
                "特に変更がなければ、\n"
                + "「財布モード終了」\n"
                + "と入力してください。"
            ])
    elif self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ステップ"] == 3:
        if self.text in ["たす", "ひく"]:
            if self.text == "たす":
                self.RUNNING_ID_DICT[self.running_id]["財布モード"]["現在の所持金"] += money
            # elif self.text == "ひく":
            else:
                if money < self.RUNNING_ID_DICT[self.running_id]["財布モード"]["現在の所持金"]:
                    self.RUNNING_ID_DICT[self.running_id]["財布モード"]["現在の所持金"] -= money
                elif money == self.RUNNING_ID_DICT[self.running_id]["財布モード"]["現在の所持金"]:
                    self.RUNNING_ID_DICT[self.running_id]["財布モード"]["現在の所持金"] -= money
                    self.reply([
                        "超ギリギリだったな...",
                        "強く生きよう。",
                        "現在あなたの所持金は\n"
                        + f"「{self.RUNNING_ID_DICT[self.running_id]['財布モード']['現在の所持金']}円」です",
                        "入力ミス等で値に変更がある場合は\n"
                        + "再度「整数」を入力後\n"
                        + "「たす」或いは「ひく」を入力してください。",
                        "特に変更がなければ「財布モード終了」と入力してください"
                    ])
                else:
                    self.reply(["破産やで...", "整数の値からやり直してね。"])
                self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ステップ"] = 2
                return
            # 理論上ありえない
            self.RUNNING_ID_DICT[self.running_id]["財布モード"]["ステップ"] = 2
            self.reply([
                "現在あなたの所持金は\n"
                + f"「{self.RUNNING_ID_DICT[self.running_id]['財布モード']['現在の所持金']}円」です",
                "まだ、入力ミス等で値に変更がある場合は\n"
                + "再度「整数」を入力後\n"
                + "「たす」或いは「ひく」を入力してください。",
                "特に変更がなければ「財布モード終了」と入力してください"
            ])
        else:
            self.reply([
                "「たす」\n"
                + "或いは\n"
                + "「ひく」\n"
                + "を入力してください。"
            ])
