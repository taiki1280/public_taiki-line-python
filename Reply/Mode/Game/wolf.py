def run(self):
    from ..game import cannot_play
    if cannot_play(self, 4, []):
        return
    elif "人狼" not in self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]:
        self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"] = {
            "ステップ": 0, "対戦回数": 1, "市民側の役職": ("市民",), "人狼側の役職": ("人狼",), "使用する役職": [], "参加者": {}
        }
    step = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["ステップ"]
    dir_participant = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["参加者"]
    participant_ids = [v for v in dir_participant]
    use_position_list = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["使用する役職"]
    position_list = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["市民側の役職"]
    position_list += self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["人狼側の役職"]
    if step == 0:
        self.reply(
            self.game_msg
            + [
                "このゲームは人狼ゲーム",
                "「ルール」\n"
                + "開発中",
                "このゲームは通常３人以上で行うゲームです。\n"
                + "まずは、ゲームをする意思を示して欲しい。\n"
                + "「参加」と入力すると準備ができます。\n"
                + "参加をしたい人は「参加」と入力してください。"
            ]
        )
        self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["ステップ"] = 1
    elif step == 1:
        if self.text == "参加":
            if self.user_id not in dir_participant:
                dir_participant.update(
                    {self.user_id: {"名前": self.display_name}}
                )
                if len([user_id for user_id in dir_participant]) >= 3:
                    self.reply([
                        "参加人数がゲーム可能な人数に達しました。",
                        participant(self),
                        "よろしければ\n"
                        + "「ゲーム開始」\n"
                        + "と入力してください。\n"
                        + "よろしくなければ、\n"
                        + "「参加」\n"
                        + "「参加取消」\n"
                        + "或いは\n"
                        + "「人狼終了」\n"
                        + "と入力してください。"
                    ])
                else:
                    self.reply([f"{self.display_name}さんの参加を確認しました。"])
            else:
                self.reply([
                    f"{self.display_name}さんは既に参加されています。",
                    "参加を取り消したい場合は、「参加取消」と入力してください"
                ])
        elif self.text in ["参加取消", "参加取り消し"]:
            if self.user_id in dir_participant:
                del(dir_participant[self.user_id])
                self.reply([f"{self.display_name}さんの参加取消をしました。"])
            else:
                self.reply([f"{self.display_name}さんは参加されていません。"])
        elif self.text == "ゲーム開始":
            if len([user_id for user_id in dir_participant]) >= 3:
                game_setting(self)
            else:
                self.reply([
                    "参加人数が適正でありません。",
                    "３人以上の参加者が必要です。",
                    participant(self),
                    "もしかして：\n"
                    + "「参加」\n"
                    + "「参加取消」\n"
                    + "「ゲーム開始」\n"
                    + "「人狼終了」"
                ])
        else:
            self.reply([
                participant(self),
                "もしかして：\n"
                + "「参加」\n"
                + "「人狼終了」"
            ])
    if step == 2:
        if self.text in position_list:
            use_position_list.append(self.text)
            game_setting(self)
        elif self.text in [f"{position}取消" for position in position_list]:
            slice_text = f"{self.text[:(len(self.text) - 2)]}"
            if slice_text in use_position_list:
                use_position_list.remove(slice_text)
                game_setting(self)
            else:
                self.reply([
                    f"{self.text[:len(self.text) - 2]}は現在設定されていません。",
                    f"{use_position_list}"
                ])
        else:
            self.reply(["初期設定をしてください。"])
    if step == 3:
        if self.type == "user":
            if self.text in use_position_list:
                self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["希望役職"] = self.text
            else:
                self.reply(["希望する役職を選択してください。"])
        else:
            request_position = []
            for participant_id in participant_ids:
                if dir_participant[participant_id] != "未選択":
                    request_position.append(dir_participant[participant_id])
            if len(request_position) == len(participant_ids):
                self.reply(check_position(self, request_position))

        dead_list = "ああ"
        self.reply([
            "恐ろしい夜がやってきました。",
            f"昨晩の犠牲者は{dead_list}さんです。",
        ])

# ゲーム開始前メソッド


def participant(self):
    dir_participant = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["参加者"]
    participant_ids = [v for v in dir_participant]
    num_of_participant_id = len(participant_ids)

    if num_of_participant_id == 0:
        return "現在、参加者はいません。"
    else:
        people = ""
        for num in range(num_of_participant_id):
            people += f"{dir_participant[participant_ids[num]]['名前']}さん\n"

        if num_of_participant_id == 1:
            people += (
                "しかいないようです。\n"
                + "非常に寂しがっています。\n"
                + "誰か参加してあげてください。"
            )
        elif num_of_participant_id == 2:
            people += "\nもう１人以上参加者を募ってください。"
        else:
            people += f"合計{num_of_participant_id}人です。"
    return (
        "現在、参加者は、\n"
        + people
    )


# ゲーム起動初期値
def game_setting(self):
    # 使用する役職リスト
    use_position_list = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["使用する役職"]
    # 参加者のディレクトリ（辞書の場所）
    dir_participant = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["参加者"]
    participant_list = [v for v in dir_participant]
    # 残りの役職の選択数
    remaining_number = len(participant_list) - len(use_position_list)
    # 全役職
    position_list = self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["市民側の役職"]
    position_list += self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["人狼側の役職"]
    add_text = ""
    # 役職の初期設定
    all_position_text = "全役職リスト"
    for position in position_list:
        all_position_text += f"\n「{position}」"
    use_position_text = "使用予定の役職リスト"

    if remaining_number < 0:
        use_position_list.remove(self.text)
    for position in use_position_list:
        use_position_text += f"\n「{position}」"

    # 最初に呼び出された時
    if self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["ステップ"] == 1:
        self.reply([
            "役職の設定を行います。\n"
            + f"下記の中からゲームで使用したい役職を{len(participant_list)}個選択してください。",
            all_position_text
        ])
        return
    elif remaining_number > 0:
        if self.text in [f"{v}取消" for v in position_list]:
            add_text = (
                f"使用する役職のうち、{self.text[:(len(self.text) - 2)]}を取り消しました。\n" +
                f"残り{remaining_number}個の役職を下記の中から設定してください。"
            )
        else:
            add_text = (
                f"使用する役職に{self.text}を追加しました。\n" +
                f"残り{remaining_number}個の役職を下記の中から設定してください。"
            )
        self.reply([
            add_text,
            all_position_text,
            use_position_text
        ])

        # 個人チャットのモードも人狼へ変更
        if self.user_id not in self.RUNNING_ID_DICT:
            self.RUNNING_ID_DICT.update({self.user_id: {"モード": "ゲームモード"}})
        self.RUNNING_ID_DICT[self.user_id]["モード"]["ゲームモード"]["ゲームの種類"] = "人狼"
        self.RUNNING_ID_DICT[self.user_id]["モード"].update("ゲームモード", "人狼")
        return
    elif remaining_number < 0:
        self.reply([
            "これ以上役職を追加できません。",
            "役職の設定の変更が必要です。",
            "「◯◯取消」と入力し役職の設定を変更してください。\n"
            + "◯◯は任意の役職",
            use_position_text
        ])
    else:
        if use_position_list.count("人狼") == 0:
            self.reply([
                "人狼がいないとこのゲームはできません。",
                "役職の設定を変更してください",
                use_position_text
            ])
        elif len(participant_list) - use_position_list.count("人狼") <= 0:
            self.reply([
                "人狼ゲームとは、人狼の数が人狼以外の人間以上であるときは人狼陣営の勝ちとなります。",
                "ゲームが成立しません。",
                "役職の設定を変更してください。",
                use_position_text
            ])
        else:
            self.reply([
                "それではゲームを開始します。",
                "個人チャットに送信された役職を確認してください。(未実装。)"
            ])
            self.RUNNING_ID_DICT[self.running_id]["ゲームモード"]["人狼"]["ステップ"] = 3


def check_position(self, request_position):
    cnt = 0
    num = request_position.count("人狼")
    return [
        "全員の希望役職を受け付けました。",
        f"今回希望役職のかぶりは{num}件でした。",
        "希望に添えなかった方はすみません。"
    ]

# 役職を配布する


def complete_position(self):
    if "人狼" not in self.RUNNING_ID_DICT[self.user_id]["ゲームモード"]:
        self.RUNNING_ID_DICT[self.user_id]["ゲームモード"]["人狼"] = {
            "ステップ": 3, "希望役職": "未選択", "自分の役職": "未選択"
        }


""" def position_setting(self):
    # 参加者のIDリストの作成
    participant_ids = [v for v in dir_participant]
    # 役職が辞書に存在しなければ、
    for participant_id in participant_ids:
        if "役職" not in dir_participant[participant_id]:
            # 全員の役職を未選択にする。
            dir_participant[participant_id]["役職"] = "未選択" """
