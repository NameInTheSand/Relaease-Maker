import os
import json
import ctypes
import sys

def change_folder_release_notes(json_file,apk_file, release_notes_file):
    with open(json_file , 'r') as f:
        data = json.loads(f.read(), strict=False)
    with open(release_notes_file, 'r') as f:
        release_notes = f.read()

    start = apk_file.find('v.') + 2
    end = apk_file.find('.apk', start)
    data["VersionName"] = apk_file[start:end]
    data["ReleaseNotes"] = "BETA BUILD. MAY CONTAIN SOME ISSUES.\n" + release_notes
    data["ApkFileName"] = apk_file

    with open(json_file , 'w') as f:
        f.write(json.dumps(data))

    return True

def change_release_notes(path,release_notes_file):
    json_file = None
    apk_file = None
    for file in os.listdir(path):
        if file.endswith('.json'):
            json_file = os.path.join(path, file)
        if file.endswith('.apk'):
            apk_file = os.path.join(path, file)

    if(json_file is not None or apk_file is not None):
        return change_folder_release_notes(json_file= json_file, apk_file= apk_file, release_notes_file= release_notes_file)
    else:
        return False

def show_end_message(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

path = os.path.realpath(os.getcwd())
for dir, subdirs, files in os.walk(path):
    for file in files:
        if file.endswith('.txt'):
            release_notes_file= os.path.join(path, file)
    for subdir in subdirs:
        if(change_release_notes(os.path.realpath(subdir),release_notes_file) == False):
            show_end_message('Operation was failed', 'One of the folders havent files', 0)
            sys.exit()
            
show_end_message(title='Operation was successful', text='All files were changed successfully', style = 0)


