# 必要なライブラリのインポート
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# OAuth認証を行う
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

# テキストをGoogleドライブに書き込む
f = drive.CreateFile({'title': 'test.txt'})
f.SetContentString('a')
f.Upload()
