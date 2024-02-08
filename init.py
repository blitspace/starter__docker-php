#! /usr/bin/env python

import glob
import re

files = glob.glob("./docker/*.*", recursive=True, , include_hidden=True)
print(files)

old_text="{{project_name}}"
new_text="qwerty-123"

for file_name in files:
    with open(file_name, 'r+') as f:
        file = f.read()
        file = re.sub(old_text, new_text, file)
        f.seek(0)
        f.write(file)
        f.truncate()


