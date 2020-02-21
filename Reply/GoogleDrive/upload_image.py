from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import re


def run(file_path, folder_id):
    # folder_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    # folder_id = '1CDiMHnxzQxzVzFf7ghMiUDO_1fbmk2hM'
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)
    f = drive.CreateFile(
        {'title': re.sub(".*/", "", file_path),
         'mimeType': 'image/png',
         'parents': [{'kind': 'drive#fileLink', 'id': folder_id}]}
    )
    f.SetContentFile(file_path)
    f.Upload()
    print(f)
    url = f"http://drive.google.com/uc?export=view&id={f['id']}"
    return url
