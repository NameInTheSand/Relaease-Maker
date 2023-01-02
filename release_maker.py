"""Module providing Function getting the folders."""
import os
import json
import ctypes
import sys

CONST_STYLE = 0

def change_folder_release_notes(json_file_path, apk_file_path, release_notes_file_path):
    """Method to change the release notes for folder files"""
    with open(json_file_path , 'r',encoding="utf8") as f:
        data = json.loads(f.read(), strict=False)
    with open(release_notes_file_path, 'r',encoding="utf8") as f:
        release_notes = f.read()

    start = apk_file_path.find('v.') + 2
    end = apk_file_path.find('.apk', start)
    data["VersionName"] = apk_file_path[start:end]
    data["ReleaseNotes"] = "BETA BUILD. MAY CONTAIN SOME ISSUES.\n" + release_notes
    data["ApkFileName"] = apk_file_path

    with open(json_file_path , 'w',encoding="utf8") as f:
        f.write(json.dumps(data))

def change_release_notes(path,release_notes_file_path):
    """Method to find the file and change release notes for them"""
    json_file_path = None
    apk_file_path = None
    for file in os.listdir(path):
        if file.endswith('.json'):
            json_file_path = os.path.join(path, file)
        elif file.endswith('.apk'):
            apk_file_path = os.path.join(path, file)

    if json_file_path or apk_file_path is not None:
        change_folder_release_notes(json_file_path, apk_file_path, release_notes_file_path)
        return True

def show_end_message(title, text):
    """Method to show the message about the operation to user"""
    return ctypes.windll.user32.MessageBoxW(CONST_STYLE, text, title, CONST_STYLE)

if __name__ == '__main__':
    path = os.path.realpath(os.getcwd())
    for _, subdirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                release_notes_file_path= os.path.join(path, file)
                break
        for subdir in subdirs:
            if change_release_notes(os.path.realpath(subdir),release_notes_file_path) is None:
                show_end_message('Operation was failed', 'One of the folders havent files')
                sys.exit()               
    show_end_message(title='Operation was successful', text='All files were changed successfully')
