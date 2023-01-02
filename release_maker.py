"""Module providing Function getting the folders."""
import os
import json
import ctypes
import sys

CONST_STYLE = 0
CONST_EVAL_RELEASE_TYPE = 0
CONST_PROD_RELEASE_TYPE = 1
CONST_BETA_BUILD_TEXT = "BETA BUILD. MAY CONTAIN SOME ISSUES.\n"


def change_folder_release_notes(
    json_file_path,
    apk_file_path,
    release_notes_file_path,
    release_type
):
    """Change the release notes for folder files"""
    with open(json_file_path, 'r', encoding="utf8") as f:
        data = json.loads(f.read(), strict=False)
    with open(release_notes_file_path, 'r', encoding="utf8") as f:
        release_notes = f.read()

    data["VersionName"] = apk_file_path.split('.', 1)[1].removesuffix('.apk')
    data["ReleaseNotes"] = CONST_BETA_BUILD_TEXT  + release_notes if release_type == CONST_EVAL_RELEASE_TYPE else release_notes
    data["ApkFileName"] = apk_file_path.split("\\")[-1]

    with open(json_file_path, 'w', encoding="utf8") as f:
        f.write(json.dumps(data))


def change_release_notes(path, release_notes_file_path, release_type):
    """Find the file and change release notes for them"""
    json_file_path = None
    apk_file_path = None
    for file in os.listdir(path):
        if file.endswith('.json'):
            json_file_path = os.path.join(path, file)
        elif file.endswith('.apk'):
            apk_file_path = os.path.join(path, file)

    if json_file_path or apk_file_path is not None:
        change_folder_release_notes(
            json_file_path=json_file_path,
            apk_file_path=apk_file_path,
            release_notes_file_path=release_notes_file_path,
            release_type=release_type
        )
        return True


def show_end_message(title, text):
    """Method to show the message about the operation to user"""
    return ctypes.windll.user32.MessageBoxW(
        CONST_STYLE, text, title, CONST_STYLE
    )


def enter_the_release_type():
    input_value = int(
        input("Please, enter the release type. 0 - eval, 1 - prod\n")
    )
    if (input_value not in [CONST_EVAL_RELEASE_TYPE, CONST_PROD_RELEASE_TYPE]):
        enter_the_release_type()
    else:
        return input_value


if __name__ == '__main__':
    path = os.path.realpath(os.getcwd())
    release_type = enter_the_release_type()
    for _, subdirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                release_notes_file_path = os.path.join(path, file)
                break
        for subdir in subdirs:
            if subdir != '.git':
                if change_release_notes(
                    path=os.path.realpath(subdir),
                    release_notes_file_path=release_notes_file_path,
                    release_type=release_type
                ) is None:
                    show_end_message(
                        title='Operation was failed',
                        text='One of the folders havent files'
                    )
                    sys.exit()
    show_end_message(
        title='Operation was successful',
        text='All files were changed successfully'
    )
