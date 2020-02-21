import random


def run(self):
    f = open("Reply/taiki/test_tamami.txt", "r", encoding="utf-8")
    data_list = []
    line = f.readline()
    while line:
        data_list.append(line.replace("\\n", "\n").rstrip())
        line = f.readline()
    f.close()
    self.RUNNING_ID_DICT[self.running_id].setdefault("たいき", 0)
    if self.text.isdigit():
        num = int(self.text)
        if len(data_list) - 1 >= num:
            self.RUNNING_ID_DICT[self.running_id]["たいき"] = num
        else:
            self.reply([
                f"最大「{len(data_list) - 1 - 6}」までだよ..."
            ])
            return
    rep = []
    cnt = self.RUNNING_ID_DICT[self.running_id]["たいき"]
    if cnt > len(data_list) - 1 - 6 or self.text == "ランダム":
        for i in range(5):
            rep.append(data_list[random.randrange(len(data_list) - 1)]),
    else:
        for i in range(5):
            rep.append(data_list[cnt + i])
            self.RUNNING_ID_DICT[self.running_id]["たいき"] += 1
    self.reply(
        rep
    )
