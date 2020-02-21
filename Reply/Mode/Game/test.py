import random


def run(self):
    self.RUNNING_ID_DICT[self.running_id]["ゲームモード"].setdefault(
        "スピード改", {"ステップ": 1, "対戦回数": 0, "バトルゾーン": [], "参加者": {}})
    self.PARTICIPANT_IDS = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード改"]["参加者"]
    self.battle_field = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード改"]["バトルゾーン"]
    self.step = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード改"]["ステップ"]
    self.round_num = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード改"]["対戦回数"]
    # 初期設定
    if self.step == 1:
        if self.text == "参加":
            join(self)
        elif self.text == "参加取消":
            cancel_join(self)
        elif self.text == "ゲーム開始":
            game_start(self)
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード改"]["ステップ"] = 2
        else:
            self.reply(
                participant(self)
                + [
                    "もしかして：\n"
                    + "「参加」\n"
                    + "「スピード改終了」"
                ]
            )
    elif self.step == 2:
        # 前回の値を引継ぎ
        self.player1_id = list(self.PARTICIPANT_IDS)[0]
        self.player2_id = list(self.PARTICIPANT_IDS)[1]
        self.p1_hand = self.PARTICIPANT_IDS[self.player1_id]["手札"]
        self.p2_hand = self.PARTICIPANT_IDS[self.player2_id]["手札"]

        if len(self.p1_hand) == 0 and len(self.p2_hand) == 0:
            fin(self, None, "draw")
        elif len(self.p1_hand) == 0:
            fin(self, self.player1_id, "win")
        elif len(self.p2_hand) == 0:
            fin(self, self.player2_id, "win")

        # ここに動きを記述していく
        # 出せるものがあるかチェック
        if check(self) == "T":
            if self.user_id == self.player1_id:
                hand_check(self, self.player1_id, self.p1_hand)
            elif self.user_id == self.player2_id:
                hand_check(self, self.player2_id, self.p2_hand)
                # 理論上ありえない
            else:
                self.reply(["What happen?", self.RUNNING_ID_DICT])
        else:
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード改"]["対戦回数"] += 1
            draw_deck(self)
    elif self.step == 3:
        if self.text == "はい":
            del(self.PARTICIPANT_IDS[self.player1_id]["山札"])
            del(self.PARTICIPANT_IDS[self.player1_id]["手札"])
            del(self.PARTICIPANT_IDS[self.player2_id]["山札"])
            del(self.PARTICIPANT_IDS[self.player2_id]["手札"])
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード改"]["対戦回数"] = 1
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード改"]["ステップ"] = 2
            game_start(self)
        elif self.text == "いいえ":
            self.reply(["最初に戻ります。", "参加する人は「参加」と入力してください。"])
            del(self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード改"])
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード改"]["ステップ"] = 1
        else:
            self.reply([
                "「はい」\n"
                + "「いいえ」\n"
                + "のいずれかを入力してください"
            ])


def check(self):
    CHECK = []
    for v in self.battle_field:
        CHECK += [v + 1, v - 1, v + 12, v - 12]
    CHECK = [v for v in CHECK if 1 <= v and v <= 13]
    for v in self.p1_hand + self.p2_hand:
        if v in CHECK:
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

    self.PARTICIPANT_IDS[self.player1_id].setdefault("山札", [])
    self.PARTICIPANT_IDS[self.player2_id].setdefault("山札", [])

    for _ in range(26):
        self.PARTICIPANT_IDS[self.player1_id]["山札"].append(
            deck.pop(random.randrange(len(deck))))
        self.PARTICIPANT_IDS[self.player2_id]["山札"].append(
            deck.pop(random.randrange(len(deck))))


def draw_hand(self, num, who):
    self.PARTICIPANT_IDS[who].setdefault("手札", [])
    deck = self.PARTICIPANT_IDS[who]["山札"]
    if len(deck) != 0:
        for _ in range(num):
            self.PARTICIPANT_IDS[who]["手札"].append(
                deck.pop(random.randrange(len(deck))))
    elif len(self.PARTICIPANT_IDS[who]["手札"]) == 0:
        fin(self, who, "win")
        self.step = 3


def disp(self, ADD_TEXT):
    field = ""
    p1_hand = ""
    p2_hand = ""
    for num in self.battle_field:
        field += f"「{num:0=2}」"
    p1_name = self.PARTICIPANT_IDS[self.player1_id]["名前"]
    p2_name = self.PARTICIPANT_IDS[self.player2_id]["名前"]

    for num in self.PARTICIPANT_IDS[self.player1_id]["手札"]:
        p1_hand += f"「{num:0=2}」"
    for num in self.PARTICIPANT_IDS[self.player2_id]["手札"]:
        p2_hand += f"「{num:0=2}」"

    self.reply(
        ADD_TEXT
        + [
            f"{p1_name}さん\n"
            + f"{p1_hand}\n\n"
            + "バトルフィールド\n"
            + f"{field}\n\n"
            + f"{p2_name}さん\n"
            + p2_hand
        ]
    )


def draw_deck(self):

    p1_deck = self.PARTICIPANT_IDS[self.player1_id]["山札"]
    p2_deck = self.PARTICIPANT_IDS[self.player2_id]["山札"]

    self.p1_hand = self.PARTICIPANT_IDS[self.player1_id]["手札"]
    self.p2_hand = self.PARTICIPANT_IDS[self.player2_id]["手札"]

    # 山札がないときは、手札から出す
    if len(p1_deck) == 0:
        left = self.p1_hand.pop(random.randrange(int(len(self.p1_hand))))
    else:
        left = p1_deck.pop(0)
    # 山札がないときは、手札から出す
    if len(p2_deck) != 0:
        right = p2_deck.pop(0)
    else:
        right = self.p2_hand.pop(random.randrange(int(len(self.p2_hand))))

    if len(self.p1_hand) == 0 and len(self.p2_hand) == 0:
        fin(self, None, "draw")
    elif len(self.p1_hand) == 0:
        fin(self, self.player1_id, "win")
    elif len(self.p2_hand) == 0:
        fin(self, self.player2_id, "win")
    self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["スピード改"]["バトルゾーン"] = [
        left, right]
    self.battle_field = [left, right]

    if self.round_num == 1:
        value_text = ["ーーーー GAME START ーーーー"]
    else:
        value_text = [
            "２人とも出せる値が無かったので\n"
            + "バトルゾーンを更新しました。",
            f"ーーーー ROUND {self.round_num:0=2} ーーーー"
        ]
    disp(self, value_text)


# ゲーム起動初期値
def game_start(self):
    if len(self.PARTICIPANT_IDS) == 2:
        self.player1_id = list(self.PARTICIPANT_IDS)[0]
        self.player2_id = list(self.PARTICIPANT_IDS)[1]
        # 二人にトランプ配布
        create_trump(self)
        # 二人が４枚引く
        draw_hand(self, 4, self.player1_id)
        draw_hand(self, 4, self.player2_id)
        # バトルフィールドに２枚置く
        draw_deck(self)
    else:
        self.reply(
            [
                "参加人数が適正でありません。",
                "２人の参加者が必要です。"
            ]
            + participant(self)
            + [
                "もしかして：\n"
                + "「参加」\n"
                + "「参加取消」\n"
                + "「ゲーム開始」\n"
                + "「スピード改終了」"
            ]
        )

# ゲーム開始前メソッド


def participant(self):
    name = ""
    ADD_TEXT = []
    for v in self.PARTICIPANT_IDS:
        print(self.PARTICIPANT_IDS[v])
        name += f"{self.PARTICIPANT_IDS[v]['名前']}さん\n"
    if len(self.PARTICIPANT_IDS) == 0:
        name = "誰も"
        add_text = "居ません。"
        ADD_TEXT = ["積極的に参加してください。"]
    elif len(self.PARTICIPANT_IDS) == 1:
        add_text = "しかいないようです。"
        ADD_TEXT = [
            "非常に寂しがっています。\n"
            + "誰か参加してあげてください。"
        ]
    elif len(self.PARTICIPANT_IDS) == 2:
        add_text = "の２人で満員です。"
    return [
        "現在、参加者は\n"
        + name
        + add_text
    ] + ADD_TEXT


def join(self):
    if self.user_id in self.PARTICIPANT_IDS:
        self.reply([
            f"{self.display_name}さんは既に参加されています。",
            "参加を取り消したい場合は、「参加取消」と入力してください。"
        ])
    elif len(self.PARTICIPANT_IDS) == 2:
        self.reply([
            "これ以上の参加はできません。",
            "「ゲームを開始」あるいは「参加取消」と入力してください。"
        ])
    else:
        ADD_TEXT = []
        self.PARTICIPANT_IDS.setdefault(
            self.user_id, {"名前": self.display_name}
        )
        if len(self.PARTICIPANT_IDS) == 2:
            ADD_TEXT = ["ゲームの参加人数が満員に達しました。"]
            ADD_TEXT += participant(self)
            ADD_TEXT += [
                "上記の参加者で宜しければ、\n"
                + "「ゲーム開始」\n"
                + "と入力してください。\n"
                + "宜しくなければ、\n"
                + "「参加取消」\n"
                + "或いは\n"
                + "「スピード改終了」\n"
                + "と入力してください。"
            ]
        self.reply(
            [f"{self.display_name}さんの参加を確認しました。"]
            + ADD_TEXT
        )


def cancel_join(self):
    if self.user_id in self.PARTICIPANT_IDS:
        del(self.RUNNING_ID_DICT[self.running_id]
            ["ゲームモード"]["スピード改"]["参加者"][self.user_id])
        self.reply([f"{self.display_name}さんの参加を取り消しました。"])
    else:
        self.reply([f"{self.display_name}さんは参加されていません。"])


def hand_check(self, who, hand):
    # 手札チェック
    name = self.PARTICIPANT_IDS[who]["名前"]
    if int(self.text) in hand:
        for num in self.battle_field:
            if int(self.text) == num - 1 or int(self.text) == num + 1 or int(self.text) == num - 12 or int(self.text) == num + 12:
                self.battle_field[self.battle_field.index(
                    num)] = int(self.text)
                self.PARTICIPANT_IDS[who]["手札"].pop(hand.index(int(self.text)))
                draw_hand(self, 1, who)
                disp(self, [])
                # disp(self, [f"{name}さんが「{self.text}」を出しました"])
                break
        else:
            value_text = [
                f"{name}さん\n"
                + f"「{self.text}」を出せる場所はありません"
            ]
            disp(self, value_text)
    else:
        value_text = [
            f"{name}さん\n"
            + f"「{self.text}」は存在しません"
        ]
        disp(self, value_text)


def fin(self, who_id, result):
    if result == "win":
        name = self.PARTICIPANT_IDS[who_id]["名前"]
        value = f"{name}さんの勝利"
    else:
        value = "この勝負は引き分け"
    self.quick_reply(
        [
            f"{value}です",
            "もう一度同じ人とプレイしますか？\n"
            + "「はい」\n"
            + "「いいえ」"
        ],
        ["はい", "いいえ"]
    )
    self.step = 3
