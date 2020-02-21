from . import mistake
import random
import re


# 電卓モード
def run(self):
    self.RUNNING_ID_DICT[self.running_id].setdefault(
        "電卓モード", {
            "入力値": 0,
            "最後の答え": 0,
            "ミス回数": 1,
            "ステップ": 1
        }
    )
    num_of_mistake = self.RUNNING_ID_DICT[self.running_id]["電卓モード"]["ミス回数"]
    OP = ["たす", "ひく", "かける", "わる", "あまり"]
    # 電卓モードの計算処理
    if self.RUNNING_ID_DICT[self.running_id]["電卓モード"]["ステップ"] == 1:
        result = re.search((r"\d+\.\d+|\d+"), self.text)
        # if self.text.isdigit():
        if result:
            input_num = float(result.group())
            input_num = decimal_normalize(input_num)
            self.RUNNING_ID_DICT[self.running_id]["電卓モード"]["入力値"] = input_num
            self.RUNNING_ID_DICT[self.running_id]["電卓モード"]["ミス回数"] = 1
            self.RUNNING_ID_DICT[self.running_id]["電卓モード"]["ステップ"] = 2
            op = ""
            for value in OP:
                op += f"「{value}」"
            self.quick_reply(
                [
                    f"{input_num}\n"
                    + "を検出しました。",
                    f"{op}\n"
                    + "の何れかを入力してください"
                ],
                OP
            )
        else:
            num1 = random.randrange(1, 5000)
            num2 = random.randrange(5000, 10000)
            mistake.run(self, num_of_mistake, "数字", num1, num2)
    elif self.RUNNING_ID_DICT[self.running_id]["電卓モード"]["ステップ"] == 2:
        input_num = self.RUNNING_ID_DICT[self.running_id]["電卓モード"]["入力値"]
        # 演算記号の処理
        # ミス時
        print(input_num)
        print(self.text)
        if self.text not in OP:
            op1 = random.choice(OP)
            op2 = random.choice([v for v in OP if v != op1])
            print(op2)
            mistake.run(self, num_of_mistake, "演算子", op1, op2)
        elif self.text in ["わる", "あまり"] and input_num == 0:
            self.reply(["0による除算は数学上不可能です。", "別の演算子を入力してください"])
            self.RUNNING_ID_DICT[self.running_id]["電卓モード"]["ミス回数"] = 1
        elif self.text in OP:
            self.reply(calc(self, input_num, self.text))
            self.RUNNING_ID_DICT[self.running_id]["電卓モード"]["ステップ"] = 1


def calc(self, v1, input_op):
    if input_op == "たす":
        op = "+"
        str_op = "+"
    elif input_op == "ひく":
        op = "-"
        str_op = "-"
    elif input_op == "かける":
        op = "*"
        str_op = "×"
    elif input_op == "わる":
        op = "/"
        str_op = "÷"
    elif input_op == "あまり":
        op = "%"
        str_op = "mod"
    ans_before = self.RUNNING_ID_DICT[self.running_id]["電卓モード"]["最後の答え"]
    last_ans = eval(f"{ans_before} {op} {v1}")
    last_ans = decimal_normalize(last_ans)
    answer = f"{ans_before} {str_op} {v1} = {last_ans}"
    self.RUNNING_ID_DICT[self.running_id]["電卓モード"]["最後の答え"] = last_ans
    return [
        "演算します",
        answer,
        f"次に{last_ans}続けて演算したい数値を入力してください"
    ]


def decimal_normalize(num):
    text = str(num)
    while True:
        if ("." in text and text[-1] == "0") or (text[-1] == "."):
            text = text[:-1]
            continue
        break
    return text
