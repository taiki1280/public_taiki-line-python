from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
FILES = drive.ListFile().GetList()

print(len(FILES))
for f in drive.ListFile({'q': 'title = "file1"'}).GetList():
    print(f['title'], '  \t', f['id'])
for f in FILES:
    print(f['title'])
    print(f['id'])
