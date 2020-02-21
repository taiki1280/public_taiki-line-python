import random


# 相談モード
def run(self):
    a = ["そうなんだね", "それはしんどかったね", "よく頑張ってるね", "苦しいよね",
         "辛いよね", "偉い偉い", "そういうときもあるよね", "うんうん。"]
    self.reply([a[random.randrange(len(a))]])
