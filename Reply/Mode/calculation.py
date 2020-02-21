from . import mistake
import random


# 計算モード
def run(self):

    self.RUNNING_ID_DICT[self.running_id].setdefault("計算モード", {
        "ミス回数": 1,
        "ステップ": 1,
        "１つ目の数値": "未選択",
        "演算子": "未選択"
    })
    miss_num = self.RUNNING_ID_DICT[self.running_id]["計算モード"]["ミス回数"]
    ran_num1 = f"{random.randrange(1, 5000)}"
    ran_num2 = f"{random.randrange(5000, 10000)}"
    num1 = self.RUNNING_ID_DICT[self.running_id]["計算モード"]["１つ目の数値"]
    op = self.RUNNING_ID_DICT[self.running_id]["計算モード"]["演算子"]
    if self.RUNNING_ID_DICT[self.running_id]["計算モード"]["ステップ"] == 1:
        if self.text.isdigit():
            self.RUNNING_ID_DICT[self.running_id]["計算モード"]["１つ目の数値"] = self.text
            self.RUNNING_ID_DICT[self.running_id]["計算モード"]["ミス回数"] = 1
            self.RUNNING_ID_DICT[self.running_id]["計算モード"]["ステップ"] = 2
            self.reply([
                "「たす」「ひく」「かける」「わる」「あまり」\n"
                + "の何れかを入力してください"
            ])
        else:
            mistake.run(self, miss_num, "数字", ran_num1, ran_num2)
    elif self.RUNNING_ID_DICT[self.running_id]["計算モード"]["ステップ"] == 2:
        # 演算記号の処理
        OP_ARRAY = ["たす", "ひく", "かける", "わる", "あまり"]
        if self.text in OP_ARRAY:
            if self.text == "たす":
                val_op = "+"
            elif self.text == "ひく":
                val_op = "-"
            elif self.text == "かける":
                val_op = "*"
            elif self.text == "わる":
                val_op = "/"
            elif self.text == "あまり":
                val_op = "%"
            # 理論上ありえない
            else:
                self.reply([num1 + self.text])
            self.RUNNING_ID_DICT[self.running_id]["計算モード"]["演算子"] = val_op
            self.reply(["２つ目の数値を入力してください"])
            self.RUNNING_ID_DICT[self.running_id]["計算モード"]["ステップ"] = 3
        else:
            max = len(OP_ARRAY) - 1
            ran_op1 = OP_ARRAY[random.randrange(1, max / 2)]
            ran_op2 = OP_ARRAY[random.randrange(max / 2, max)]
            mistake.run(self, miss_num, "演算子", ran_op1, ran_op2)
    elif self.RUNNING_ID_DICT[self.running_id]["計算モード"]["ステップ"] == 3:
        if self.text.isdigit():
            num2 = self.text
            if num2 == "0" and val_op in ["/", "%"]:
                self.reply(["0による除算は数学上不可能です。", "別の数値を入力してください"])
                self.RUNNING_ID_DICT[self.running_id]["計算モード"]["ミス回数"] = 1
                return
            self.RUNNING_ID_DICT[self.running_id]["計算モード"]["ミス回数"] = 1
            # 計算モードの処理

            def calc(v1, op, v2):
                ans_after = eval(v1 + op + v2)
                answer = f"{v1} {op} {v2} = {ans_after}"
                return answer
            self.RUNNING_ID_DICT[self.running_id]["計算モード"]["ステップ"] = 1
            self.reply([
                "演算します",
                calc(num1, op, num2),
                "終了したい場合は、\n"
                + "「計算モード終了」\n"
                "と入力してください。",
                "続けて実行する場合は１つ目の数値を入力してください"
            ])
        else:
            mistake.run(self, miss_num, "数字", ran_num1, ran_num2)
