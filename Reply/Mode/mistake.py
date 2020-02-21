# 電卓モード、計算モードミス時
def run(self, i, num_or_op, value1, value2):
    self.RUNNING_ID_DICT[self.running_id][self.mode]["ミス回数"] += 1
    MSG_ARRAY = [f"{i}回目の失敗!!"]
    if i == 1:
        MSG_ARRAY += (
            f"それは{num_or_op}ではありません。",
            f"{num_or_op}を入力してください\n"
            + f"例）「{value1}」「{value2}」"
        )
    elif i == 2:
        MSG_ARRAY += (
            f"...それも{num_or_op}じゃないよ？？",
            f"{num_or_op}を入力してね！\n"
            + f"例）「{value1}」「{value2}」"
        )
    elif i <= 4:
        MSG_ARRAY += (
            f"ん～{num_or_op}じゃないなぁ...",
            f"{num_or_op}にしようか？？\n"
            + f"例）「{value1}」「{value2}」"
        )
    elif i <= 6:
        MSG_ARRAY += (
            f"えっと、{num_or_op}って分かる？？",
            f"「{value1}」とか「{value2}」って小学校で習わなかった？？"
        )
    elif i <= 8:
        MSG_ARRAY += (
            "さては計算する気が無い！？",
            f"{num_or_op}がいいなぁ。だいぶ疲れてきたよzZ"
        )
    elif i < 10:
        MSG_ARRAY += (
            "いい加減にしろw",
            f"{num_or_op}入れろって言ってるやんかww",
            f"次やったら{self.mode}終了するからな！？！？！？"
        )
    else:
        self.finish()
        return
    self.reply(MSG_ARRAY)
