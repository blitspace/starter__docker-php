#!/bin/bash

old_string="project-123"
skip_extension="sh"

echo "Please enter the project name (all lower case with - for space):"
read new_string

if [ -z "$new_string" ]
then
  echo "Project name is empty. Please enter a valid string."
  return 1
fi

find ./ -type f ! -name "*.$skip_extension" -exec sed -i "s/$old_string/$new_string/g" {} \;
