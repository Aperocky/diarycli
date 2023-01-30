import os
import sys
import argparse
from pathlib import Path
from subprocess import call
from datetime import date
from datetime import datetime


DIARY_DIR = os.environ.get("DIARY_DIR")
DIARY_EDITOR = os.environ.get("DIARY_EDITOR")
if DIARY_DIR is None:
    DIARY_DIR = os.path.join(Path.home(), "diary")
if DIARY_EDITOR is None:
    DIARY_EDITOR = "vim"


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise SystemExit(e)


def edit_entry(target_date = None):
    if not target_date:
        target_date = date.today()
    entry_directory = os.path.join(DIARY_DIR, str(target_date.year), "{:02}".format(target_date.month))
    if not os.path.isdir(entry_directory):
        os.makedirs(entry_directory)
    date_str = target_date.strftime("%Y-%m-%d")
    file_name = date_str + ".md"
    entry_path = os.path.join(os.path.join(entry_directory, file_name))
    entry_exist = False
    if os.path.isfile(entry_path):
        entry_exist = True
    with open(entry_path, "a") as entry:
        if not entry_exist:
            entry.write(datetime.strftime(target_date, "## %Y-%m-%d, %A"))
        entry.flush()
        call([DIARY_EDITOR, entry_path])


def cat_entry():
    target_date = date.today()
    entry_directory = os.path.join(DIARY_DIR, str(target_date.year), "{:02}".format(target_date.month))
    file_name = target_date.strftime("%Y-%m-%d") + ".md"
    entry_path = os.path.join(os.path.join(entry_directory, file_name))
    if os.path.isfile(entry_path):
        with open(entry_path, "r") as entry:
            print(entry.read())
    else:
        print("Diary for today not created yet")


def main():
    args = sys.argv[1:]
    if not args:
        edit_entry()
    elif args[0] == "cat":
        cat_entry()
    else:
       edit_entry(parse_date(args[0]))


if __name__ == "__main__":
    main()
