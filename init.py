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
import progressbar
# from tqdm import tqdm

pbar = None

def show_progress(block_num, block_size, total_size):
    global pbar

    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


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
    move_files("./templates/docker", "./", rename_templates=True)
    search_replace_files("./docker/*.*", old_text, new_text_processed)
    search_replace_files("./docker/.env", old_text, new_text_processed)
    search_replace_files("./README.md", old_text, new_text)


def move_files(_src: str, _dest, rename_templates=False) -> None:
    global pbar

    files = sorted([f for f in glob.glob(_src + "/**/*.*", recursive=True)])

    if verbose:
        pp.pprint(files)

    if pbar is None:
        pbar = progressbar.ProgressBar(max_value=len(files))
        pbar.start()

    for indx, f in enumerate(files):
        f = f.replace("\\", "/")
        d = f"{_dest}/" + "/".join(f.split("/")[3:-1])

        if not Path(d).exists():
            if verbose:
                print(Fore.BLUE + "Creating directory", d, Fore.RESET)
            Path(d).mkdir(parents=True, exist_ok=True)

        dest = _dest + f.replace(_src, "")

        if rename_templates:
            dest = dest.replace(".template", "")

        if verbose:
            print(Fore.GREEN + "Moving: ", f, "->", dest, Fore.RESET)

        shutil.move(f, dest)
        pbar.update(indx)

    pbar.finish()
    pbar = None


def process_wp():
    global pbar

    shutil.copy('./templates/wp-config-sample.php.template', './src/wp-config.php')
    search_replace_files("./src/wp-config.php", old_text, new_text_processed)

    # Create temp directory if not exists
    Path(temp_path).mkdir(parents=True, exist_ok=True)

    if Path(f"{temp_path}/latest.zip").exists():
        print(f"\nUsing {temp_path}/latest.zip")
    else:
        print(Fore.GREEN + "\nDownloading latest WordPress...", Fore.RESET)
        urllib.request.urlretrieve(wordpress_download_link, f"{temp_path}/latest.zip", show_progress)

    print(Fore.GREEN + "\nExtracting WordPress files...", Fore.RESET)

    with ZipFile(f"{temp_path}/latest.zip", 'r') as zip_obj:
        files = zip_obj.infolist()

        if pbar is None:
            pbar = progressbar.ProgressBar(max_value=len(files))
            pbar.start()

        for indx, file in enumerate(files):
            zip_obj.extract(file, temp_path)
            pbar.update(indx)

        pbar.finish()
        pbar = None

    print(Fore.GREEN + "\nMoving files...", Fore.RESET)
    move_files(f"{temp_path}/wordpress", "./src")


    print("\nRemove temp directory? [y/N]", end=" ")
    remove_temp_dir = input()

    if not remove_temp_dir == "N":
        print(Fore.GREEN + "Removing temp directory...", Fore.RESET)
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

    print("\n")
    print("=================================")
    print("Init docker")
    print("=================================")
    print("cd docker")
    print("docker compose up -d")
