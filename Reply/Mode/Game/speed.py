import random


def check(battle_field, p1_hand, p2_hand):
    for one_of_battle_field in battle_field:
        for hand in [p1_hand, p2_hand]:
            for p1 in hand:
                if (
                    one_of_battle_field + 1 == p1
                    or one_of_battle_field - 1 == p1
                    or one_of_battle_field + 12 == p1
                    or one_of_battle_field - 12 == p1
                ):
                    return "T"
    return "F"


def create_trump(self):
    # 山札を作成
    deck = []
    # 数値を設定
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    # スート分追加
    for _ in range(4):
        deck += num
    # 二人にトランプを配る
    user_list = [v for v in self.RUNNING_ID_DICT[self.running_id]
                 ["ゲームモード"]["スピード"]["参加者"]]
    p1_id = user_list[0]
    p2_id = user_list[1]

    self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p1_id].update(
        {"山札": []}
    )
    self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p2_id].update(
        {"山札": []}
    )

    for _ in range(26):
        self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p1_id]["山札"].append(
            deck.pop(random.randrange(len(deck))))
        self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p2_id]["山札"].append(
            deck.pop(random.randrange(len(deck))))


def draw_hand(self, num, who):

    if "手札" not in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][who]:
        self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][who].update(
            {"手札": []})
    deck = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][who]["山札"]

    if len(deck) != 0:
        for _ in range(num):
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][who]["手札"].append(
                deck.pop(random.randrange(len(deck))))
    elif len(self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][who]["手札"]) == 0:
        fin(self, who, "win")
        self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["ステップ"] = 3


def disp(self, add_text):
    global battle_field
    field = ""
    for num in battle_field:
        field += "「{:0=2}」".format(num)

    user_list = [
        v for v in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]
    ]
    p1_id = user_list[0]
    p2_id = user_list[1]

    p1_hand = ""
    p2_hand = ""

    p1_name = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p1_id]["名前"]
    p2_name = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p2_id]["名前"]

    for num in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p1_id]["手札"]:
        p1_hand += "「{:0=2}」".format(num)
    for num in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p2_id]["手札"]:
        p2_hand += "「{:0=2}」".format(num)

    if add_text != "":
        self.reply([
            add_text,
            "{}さん\n".format(p1_name)
            + p1_hand + "\n\n"
            + "バトルフィールド\n"
            + field + "\n\n"
            "{}さん\n".format(p2_name)
            + p2_hand
        ])
    else:
        self.reply([
            "{}さん\n".format(p1_name)
            + p1_hand + "\n\n"
            + "バトルフィールド\n"
            + field + "\n\n"
            "{}さん\n".format(p2_name)
            + p2_hand
        ])


def draw_deck(self):
    user_list = [v for v in self.RUNNING_ID_DICT[self.running_id]
                 ["ゲームモード"]["スピード"]["参加者"]]
    p1_id = user_list[0]
    p2_id = user_list[1]

    p1_deck = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p1_id]["山札"]
    p2_deck = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p2_id]["山札"]

    p1_hand = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p1_id]["手札"]
    p2_hand = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p2_id]["手札"]

    # 山札がないときは、手札から出す
    if len(p1_deck) == 0:
        left = p1_hand.pop(random.randrange(int(len(p1_hand))))
    else:
        left = p1_deck.pop(0)
    # 山札がないときは、手札から出す
    if len(p2_deck) != 0:
        right = p2_deck.pop(0)
    else:
        right = p2_hand.pop(random.randrange(int(len(p2_hand))))

    if len(p1_hand) == 0 and len(p2_hand) == 0:
        fin(self, None, "draw")
    elif len(p1_hand) == 0:
        fin(self, p1_id, "win")
    elif len(p2_hand) == 0:
        fin(self, p2_id, "win")

    global battle_field
    battle_field = [left, right]

    cnt = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["対戦回数"]
    if cnt == 1:
        value_text = "ーーーー GAME START ーーーー"
    else:
        # value_text = "２人とも出せる値が無かったので\n山札をめくりました。\n"
        value_text = "ーーーー ROUND {:0=2} ーーーー".format(cnt)
    disp(self, value_text)


# ゲーム起動初期値
def game_start(self):
    user_list = [v for v in self.RUNNING_ID_DICT[self.running_id]
                 ["ゲームモード"]["スピード"]["参加者"]]
    p1_id = user_list[0]
    p2_id = user_list[1]
    # 二人にトランプ配布
    create_trump(self)
    # 二人が４枚引く
    draw_hand(self, 4, p1_id)
    draw_hand(self, 4, p2_id)
    # バトルフィールドに２枚置く
    draw_deck(self)


# ゲーム開始前メソッド
def participant(self):
    if len([name for name in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]]) == 0:
        return "現在、参加者はいません。"
    elif len([name for name in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]]) == 1:
        return (
            "現在、参加者は\n"
            + self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][
                [
                    name for name in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]
                ]
                [0]
            ]
            ["名前"]
            + "さんしかいないようです。\n"
            "非常に寂しがっています。\n"
            + "誰か参加してあげてください。"
        )
    else:
        return (
            "現在、参加者は、\n"
            + self.RUNNING_ID_DICT[self.running_id]
            ["ゲームモード"]["スピード"]["参加者"][
                [
                    name for name in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]
                ]
                [0]
            ]
            ["名前"]
            + "さん\n"
            + self.RUNNING_ID_DICT[self.running_id]
            ["ゲームモード"]["スピード"]["参加者"][
                [
                    name for name in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]
                ]
                [1]
            ]
            ["名前"]
            + "さん\n"
            "です。"
        )


def run(self):
    if "スピード" not in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]:
        self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"] = {
            "ステップ": 1, "対戦回数": 1, "参加者": {}}
    if self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["ステップ"] == 1:
        if self.text == "参加":
            if len([user_id for user_id in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]]) <= 1:
                if self.USER_ID not in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]:
                    self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"].update(
                        {self.USER_ID: {"名前": self.display_name}})
                    if len([user_id for user_id in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]]) == 2:
                        self.reply([
                            "ゲームの参加人数が満員に達しました。",
                            participant(self),
                            "よろしければ\n"
                            + "「ゲーム開始」\n"
                            + "と入力してください。\n"
                            + "よろしくなければ、\n"
                            + "「参加取消」\n"
                            + "或いは\n"
                            + "「スピード終了」\n"
                            + "と入力してください。"
                        ])
                    else:
                        self.reply(
                            ["{}さんの参加を確認しました。".format(self.display_name)])
                else:
                    self.reply(["{}さんは既に参加されています。".format(self.display_name),
                                "参加を取り消したい場合は、「参加取消」」と入力してください"])
            else:
                self.reply(["これ以上の参加はできません。",
                            "「ゲームを開始」あるいは「参加取消」と入力してください"])
        elif self.text == "参加取消":
            if self.USER_ID in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]:
                self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"].pop(
                    self.USER_ID)
                self.reply(["{}さんの参加取消をしました。".format(self.display_name)])
            else:
                self.reply(["{}さんは参加されていません。".format(self.display_name)])
        elif self.text == "ゲーム開始":
            if len([user_id for user_id in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]]) == 2:
                game_start(self)
                self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["ステップ"] = 2
            else:
                self.reply([
                    "参加人数が適正でありません。",
                    "２人の参加者が必要です。",
                    participant(self),
                    "もしかして：\n"
                    + "「参加」\n"
                    + "「参加取消」\n"
                    + "「ゲーム開始」\n"
                    + "「スピード終了」"
                ])
        else:
            self.reply([
                participant(self),
                "もしかして：\n"
                + "「参加」\n"
                + "「スピード終了」"
            ])
    elif self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["ステップ"] == 2:
        # 前回の値を引継ぎ
        user_list = [
            name for name in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]
        ]
        p1_id = user_list[0]
        p2_id = user_list[1]
        p1_hand = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p1_id]["手札"]
        p2_hand = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p2_id]["手札"]

        if len(p1_hand) == 0 and len(p2_hand) == 0:
            fin(self, None, "draw")
        elif len(p1_hand) == 0:
            fin(self, p1_id, "win")
        elif len(p2_hand) == 0:
            fin(self, p2_id, "win")

        # self.reply("現在開発中です")
        # ここに動きを記述していく
        # 出せるものがあるかチェック
        global battle_field
        if check(battle_field, p1_hand, p2_hand) == "T":
            if self.USER_ID == p1_id:
                hand_check(self, p1_id, p1_hand)
            elif self.USER_ID == p2_id:
                hand_check(self, p2_id, p2_hand)
                # 理論上ありえない
            else:
                self.reply(["What happen?", self.RUNNING_ID_DICT])
        else:
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["対戦回数"] += 1
            draw_deck(self)
    elif self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["ステップ"] == 3:
        if self.text == "はい":
            user_list = [
                v for v in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"]
            ]
            p1_id = user_list[0]
            p2_id = user_list[1]
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p1_id].pop(
                "山札"
            )
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p1_id].pop(
                "手札"
            )
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p2_id].pop(
                "山札"
            )
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][p2_id].pop(
                "手札"
            )
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["対戦回数"] = 1
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["ステップ"] = 2
            game_start(self)
        elif self.text == "いいえ":
            self.reply(["最初に戻ります。", "参加する人は「参加」と入力してください。"])
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"].pop("スピード")
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["ステップ"] = 1
        else:
            self.reply([
                "「はい」\n"
                + "「いいえ」\n"
                + "のいずれかを入力してください"
            ])


def hand_check(self, who, hand):
    global battle_field
    # 手札チェック
    name = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][who]["名前"]
    if int(self.text) in hand:
        for num in battle_field:
            if int(self.text) == num - 1 or int(self.text) == num + 1 or int(self.text) == num - 12 or int(self.text) == num + 12:
                battle_field[battle_field.index(num)] = int(self.text)
                self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][who]["手札"].pop(
                    hand.index(int(self.text)))
                draw_hand(self, 1, who)
                disp(self, "")
                break
        else:
            value_text = (
                "{}さん\n".format(name)
                + "「{}」を出せる場所はありません".format(self.text)
            )
            disp(self, value_text)
    else:
        value_text = (
            "{}さん\n".format(name)
            + "「{}」は存在しません".format(self.text)
        )
        disp(self, value_text)


def fin(self, who_id, result):
    if result == "win":
        name = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["参加者"][who_id]["名前"]
        value = "{}さんの勝利".format(name)
    else:
        value = "この勝負は引き分け"
    self.reply([
        "{}です".format(value),
        "もう一度同じ人とプレイしますか？\n"
        + "「はい」\n"
        + "「いいえ」"
    ])
    self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード"]["ステップ"] = 3
