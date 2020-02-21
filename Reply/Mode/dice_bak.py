from . import mistake
import random


def run(self):
    if "ダイスモード" not in self.RUNNING_ID_DICT[self.running_id]:
        self.RUNNING_ID_DICT[self.running_id]["ダイスモード"] = {"ミス回数": 1}
        self.reply(
            self.value
        )
        return
    if self.text.isdigit() == True:
        end_count = int(self.text)
        if end_count == 0:
            self.reply(["このダイスが振られる事はありませんでした。。。",
                        "次こそは振る場合は数値を入力してください。",
                        "終了したい場合は「ダイスモード終了」入力してください。"])
        elif end_count <= 222:
            text = ""
            for i in range(1, end_count + 1):
                if i != end_count:
                    text += str(i).zfill(3) + "回目. " + \
                        str(random.randrange(1, 7)) + "\n"
                else:
                    text += str(i).zfill(3) + "回目. " + \
                        str(random.randrange(1, 7))
            self.reply(["ダイスを" + str(end_count) + "回振った結果です。",
                        text,
                        "再度振る場合は数値を入力してください。",
                        "終了したい場合は「ダイスモード終了」入力してください。"])
        else:
            self.reply(["申し訳ありません。",
                        "222回を超える回数は振ることができません。",
                        "222回以下を繰り返し実行してください。"])
    else:
        mistake.run(self, self.RUNNING_ID_DICT[self.running_id]["ダイスモード"]["ミス回数"], "整数", str(
            random.randrange(1, 100)), str(random.randrange(100, 223)))
