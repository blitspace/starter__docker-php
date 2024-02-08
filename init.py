#! /usr/bin/env python

import glob
import re


def search_replace_files(pattern: list | str, old_text: str, new_text: str) -> None:
    files = glob.glob(pattern, recursive=True) \

    print(files)

    for file_name in files:
        with open(file_name, 'r+') as f:
            file = f.read()
            file = re.sub(old_text, new_text, file)

            f.seek(0)
            f.write(file)
            f.truncate()


old_text="{{project_name}}"

print("Please input the project name:")
new_text=input()
new_text_processed = new_text.replace(" ", "-")
new_text_processed = new_text_processed.lower()

if not new_text:
    print("Please input a valid project name")
    exit(1)

search_replace_files("./docker/*.*", old_text, new_text_processed)
search_replace_files("./docker/.env", old_text, new_text_processed)
search_replace_files("./README.md", old_text, new_text)
