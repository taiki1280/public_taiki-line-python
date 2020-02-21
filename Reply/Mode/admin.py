import random


# 管理者モード
def run(self):
    # 大樹の場合
    if self.event.source.user_id == "Uffc2e609077732c505aae085ba524938":
        # グループの場合
        if self.text == "Groupid":
            if self.type == "group":
                self.reply(["グループID", f"{self.event.source.group_id}"])
            else:
                self.reply(["ここのタイプは", self.type])
            # ルームの場合
        elif self.text == "Roomid":
            if self.type == "room":
                self.reply(["ルームID", f"{self.event.source.room_id}"])
        elif self.text == "の":
            a = ["あ", "い", "う", "え", ]
            self.reply([a[random.randrange(0, len(a), 1)]])
        elif self.text == "event":
            self.reply([str(self.event)])
        elif self.text == "a":
            self.reply([str(self.event.source.user_id)])
        elif self.text == "あ":
            self.reply([str(self.RUNNING_ID_DICT)])
        elif self.text == "い":
            language_list = ["Ruby", "Python", "PHP", "Java", "C"]
            self.quick_reply(["テスト"], language_list)
        else:
            self.reply(["たいきの実験"])
        # 陽太の場合
    elif self.event.source.user_id == "Udc648d55708d9becb3a53fa8e058d2e9":
        self.reply(["貴方は陽太", "通称ジブリールです。"])
    elif self.event.source.user_id == "U8b0e55a1ef2c491311ce7f979f082510":
        self.reply(["貴方は大倉 聖也", "たいきの現在のクラスメイトです。"])
    else:
        self.reply([
            "たいきに登録された人間以外は扱うことができません。",
            "貴方のユーザーIDの取得が完了しました。",
            str(self.event.source.user_id)
        ])
