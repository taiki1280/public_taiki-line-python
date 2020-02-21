import re


def run(self):
    path = plot_graph(self)
    from ..GoogleDrive import upload_image
    path = upload_image.run(path, "1CDiMHnxzQxzVzFf7ghMiUDO_1fbmk2hM")
    self.reply_img(path)


def plot_graph(self):
    # y = "1 / 20 * x ** 3"
    import numpy as np
    import matplotlib.pyplot as plt
    lim = 10
    x = np.arange(-lim, lim, 0.1)
    # y = value
    y = eval(change_str(self.text))
    # y = exec(value)
    plt.xlim([-lim, lim])  # y軸の表示範囲を -10 から 10 に限定
    plt.ylim([-lim, lim])  # y軸の表示範囲を -10 から 10 に限定
    plt.gca().set_aspect("equal", adjustable="box")  # 方眼紙テクニック
    plt.xlabel("x")  # 横軸のラベル
    plt.ylabel("y",  rotation=0)  # 縦軸のラベル
    plt.grid()  # グリッド（目盛り線）を表示
    plt.plot(x, y)
    save_path = f"Reply/GoogleDrive/graph/{change_filename(self.text)} のグラフ.png"
    # 出来たグラフをpng保存
    plt.savefig(save_path)
    # pltを終了
    plt.close()
    return save_path


def change_str(text):
    text = text.replace(" ", "")
    text = text.replace("y=", "")
    text = text.replace("+", " + ")
    print(text)
    text = re.sub(r"(\d)x", r"\1 * x", text)
    # result = re.search()
    # if result:
    # a = result.group()
    # a = re.sub(r"=", "", a)
    # text = re.sub("y.*=", "", text)
    print(text)
    return text


def change_filename(text):
    text = text.replace(" ", "")
    text = text.replace("y=", "")
    text = re.sub(r"\*\*(x|\d+)", r"の\1乗", text)
    text = text.replace("*", "")
    text = text.replace("+", " + ")
    text = f"y = {text}"
    print(text)
    return text
