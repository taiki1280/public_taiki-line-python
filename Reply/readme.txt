➀token.txtを開く
  自分のチャンネルアクセストークンと
  チャンネルシークレットを入力してください。

➁ngrok.batを起動
  httpsから始まるurlをコピーし、
  /callback
  を追記してください。
  例）https://(ランダム).ngrok.io/callback


➂LINEDevelopersにアクセスし
  https://developers.line.biz/ja/

reply.pyの__init__には最低限この辺りは使うだろうと個人的に思ったものだけを残しました。
Replyクラス及びreply関数は僕の自作なので、関数名を変えるなり、削除するなり、そのまま使うなりして下さい！

reply(taiki).pyを置いていますが参照ファイルはないので飽くまで僕がこう使っているというだけです

次にReplyフォルダ内の