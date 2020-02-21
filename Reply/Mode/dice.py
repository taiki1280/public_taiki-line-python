from . import mistake
import random


def run(self):
    self.RUNNING_ID_DICT[self.running_id].setdefault("ダイスモード", {"ミス回数": 1})
    if self.text.isdigit():
        end_count = int(self.text)
        if end_count == 0:
            self.reply(["このダイスが振られる事はありませんでした。。。",
                        "次こそは振る場合は数値を入力してください。",
                        "終了したい場合は「ダイスモード終了」入力してください。"])
        elif end_count <= 222:
            text = ""
            for i in range(end_count):
                # i >>> 0 ~ 5
                # str_i >>> 1 ~ 6
                text += f"{i+1:03}回目. {random.randrange(6) + 1}"
                if i != end_count - 1:
                    text += "\n"
            self.reply([f"ダイスを{end_count}回振った結果です。",
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
