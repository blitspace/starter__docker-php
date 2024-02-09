#! /usr/bin/env python

import glob
import os
import re
import urllib.request
from zipfile import ZipFile 
from pathlib import Path
import shutil
from colorama import Fore
from pprint import PrettyPrinter


def search_replace_files(pattern: list | str, old_text: str, new_text: str) -> None:
    files = glob.glob(pattern, recursive=True)

    for file_name in files:
        with open(file_name, 'r+') as f:
            file = f.read()
            file = re.sub(old_text, new_text, file)

            f.seek(0)
            f.write(file)
            f.truncate()

def process_docker_files():
    search_replace_files("./docker/*.*", old_text, new_text_processed)
    search_replace_files("./docker/.env", old_text, new_text_processed)
    search_replace_files("./README.md", old_text, new_text)


def process_wp():
    shutil.copy('./wp/wp-config-sample.php', './src/wp-config.php')
    search_replace_files("./src/wp-config.php", old_text, new_text_processed)

    # Create temp directory if not exists
    Path(temp_path).mkdir(parents=True, exist_ok=True)

    if Path(f"{temp_path}/latest.zip").exists():
        print(f"Using {temp_path}/latest.zip")
    else:
        print("\nDownloading latest WordPress...")
        urllib.request.urlretrieve(wordpress_download_link, f"{temp_path}/latest.zip")
        print("Done download...")

    print("\nExtracting WordPress files")
    with ZipFile(f"{temp_path}/latest.zip", 'r') as zip_obj: 
        zip_obj.extractall(path=temp_path) 

    files = sorted([f for f in glob.glob(f"{temp_path}/wordpress/**/*.*", recursive=True)])

    if verbose:
        pp.pprint(files)

    for f in files:
        f = f.replace("\\", "/")
        d = "./src/" + "/".join(f.split("/")[3:-1])

        # print(f)

        if not Path(d).exists():
            if verbose:
                print(Fore.BLUE, "Creating directory", d, Fore.RESET)
            Path(d).mkdir(parents=True, exist_ok=True)

        dest = "./src" + f.replace(f"{temp_path}/wordpress", "")

        if verbose:
            print(Fore.GREEN, "moving: ", f, "->", dest, Fore.RESET)

        shutil.move(f, dest)

    print("\nRemove temp directory? [Y/n]", end=" ")
    remove_temp_dir = input()

    if remove_temp_dir == "Y":
        shutil.rmtree(temp_path)


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    pp = PrettyPrinter()

    wordpress_download_link = "https://wordpress.org/latest.zip"
    temp_path = "./temp"
    verbose = False


    old_text="{{project_name}}"

    print("Please input the project name:", end=" ")
    new_text=input()
    new_text_processed = new_text.replace(" ", "-")
    new_text_processed = new_text_processed.lower()

    if not new_text:
        print("Please input a valid project name")
        exit(1)

    print("Do you want to install WordPress? [Y/n]", end=" ")
    process_wp_prompt = input()


    process_docker_files()

    if process_wp_prompt == "Y":
        process_wp()

    print("Init docker")
    print("=================================")
    print("cd docker")
    print("docker compose up -d")