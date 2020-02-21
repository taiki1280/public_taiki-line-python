import random


def run(self):
    # 初期設定
    self.RUNNING_ID_DICT[self.running_id]["ゲームモード"].setdefault(
        "じゃんけん", {"ステップ": 0, "試合回数": 1, "勝敗記録": {"勝ち": 0, "負け": 0, "あいこ": 0}})
    if self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["じゃんけん"]["ステップ"] == 0:
        print(self.game_msg)
        self.quick_reply(
            self.game_msg
            + do_janken(self),
            ["グー", "チョキ", "パー"]
        )
        self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["じゃんけん"]["ステップ"] = 1
        return
    hand = ("グー", "チョキ", "パー")
    if self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["じゃんけん"]["ステップ"] == 1:
        if self.text in hand:
            player_hand = self.text
            cpu_hand = random.choice(hand)
            self.quick_reply(
                [
                    f"{self.display_name}さんの手は{player_hand}で\n"
                    + f"CPUの手は{cpu_hand}でした。\n"
                    + judgement(
                        self, hand.index(player_hand),
                        hand.index(cpu_hand)
                    )
                ]
                + make_record(self)
                + do_janken(self),
                list(hand)
            )
        elif self.text in ["リセット", "削除"]:
            self.quick_reply(
                [
                    "本当に勝敗記録を削除しますか？\n"
                    + "「はい」\n"
                    + "「いいえ」"
                ],
                ["はい", "いいえ"]
            )
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["じゃんけん"]["ステップ"] = 2
        else:
            self.quick_reply(
                make_record(self) + do_janken(self),
                list(hand)
            )
    elif self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["じゃんけん"]["ステップ"] == 2:
        if self.text in ["はい", "いいえ"]:
            if self.text in ["はい"]:
                reset(self)
                yes_or_no = "今までのデータを全て削除しました。"
            elif self.text in ["いいえ"]:
                yes_or_no = "何もしませんでした。"
            self.quick_reply(
                [yes_or_no] + do_janken(self),
                list(hand)
            )
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["じゃんけん"]["ステップ"] = 0
        else:
            self.reply(
                ["「はい」「いいえ」の何れかを選択してください。"],
                ["はい", "いいえ"]
            )


def judgement(self, player_num, cpu_num):
    if player_num == cpu_num:
        value = "あいこ"
        result = "あいこでした！！"
    else:
        if player_num == cpu_num - 1 or player_num == cpu_num + 2:
            value = "勝ち"
        else:
            value = "負け"
        result = f"{self.display_name}さんの{value}です！"
    self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["じゃんけん"]["勝敗記録"][value] += 1
    self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["じゃんけん"]["試合回数"] += 1
    print(result)
    return result


def do_janken(self):
    return [
        f"第{self.RUNNING_ID_DICT[self.running_id]['ゲームモード']['じゃんけん']['試合回数']}回戦\n"
        + "何を出しますか？\n"
        + "「グー」\n"
        + "「チョキ」\n"
        + "「パー」"
    ]


def make_record(self):
    if self.type == "user":
        value = f"{self.display_name}さん"
    elif self.type == "group":
        value = "このグループ"
    elif self.type == "room":
        value = "このルーム"
    return [
        f"{value}の今までの記録は\n"
        + f"{self.RUNNING_ID_DICT[self.running_id]['ゲームモード']['じゃんけん']['勝敗記録']['勝ち']}勝"
        + f"{self.RUNNING_ID_DICT[self.running_id]['ゲームモード']['じゃんけん']['勝敗記録']['負け']}敗"
        + f"{self.RUNNING_ID_DICT[self.running_id]['ゲームモード']['じゃんけん']['勝敗記録']['あいこ']}分け\n"
        + "です。"
    ]


def reset(self):
    self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["じゃんけん"]["勝敗記録"] = {
        "勝ち": 0, "負け": 0, "あいこ": 0}
    self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["じゃんけん"]["試合回数"] = 1
    self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["じゃんけん"]["ステップ"] = 1
