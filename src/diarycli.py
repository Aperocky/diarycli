#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path
from subprocess import call
from datetime import date, datetime

from .templates import DIARY_TEMPLATE

class DiaryEntry:
    def __init__(self, date, content):
        self.date = date
        self.content = content

class Diary:
    def __init__(self, diary_dir=None, diary_editor=None, db_file=None):
        if diary_dir is None:
            diary_dir = os.path.join(Path.home(), "diary")
        if diary_editor is None:
            diary_editor = "vim"
        if db_file is None:
            db_file = "diary.db"

        self.DIARY_DIR = diary_dir
        self.DIARY_EDITOR = diary_editor
        self.DB_FILE = db_file
        self.commands = {}

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError as e:
            raise SystemExit(e)

    def execute(self, command, *args):
        if command in self.commands:
            self.commands[command](*args)
        else:
            print(f"Unknown command: {command}")
    


    def edit_entry(self, target_date=None):
        if not target_date:
            target_date = date.today()
        entry_directory = os.path.join(self.DIARY_DIR, str(target_date.year), "{:02}".format(target_date.month))
        if not os.path.isdir(entry_directory):
            os.makedirs(entry_directory)
        date_str = target_date.strftime("%Y-%m-%d")
        file_name = date_str + ".md"
        entry_path = os.path.join(os.path.join(entry_directory, file_name))
        entry_exist = False
        if os.path.isfile(entry_path):
            entry_exist = True
        with open(entry_path, "a") as entry:
            template_file = DIARY_TEMPLATE
            if not entry_exist:
                entry.write(datetime.strftime(target_date, "## %Y-%m-%d, %A"))
                entry.write(template_file)
            entry.flush()
            call([self.DIARY_EDITOR, entry_path])

    def cat_entry(self):
        target_date = date.today()
        entry_directory = os.path.join(self.DIARY_DIR, str(target_date.year), "{:02}".format(target_date.month))
        file_name = target_date.strftime("%Y-%m-%d") + ".md"
        entry_path = os.path.join(os.path.join(entry_directory, file_name))
        if os.path.isfile(entry_path):
            with open(entry_path, "r") as entry:
                print(entry.read())
        else:
            print("Diary for today not created yet")

if __name__ == "__main__":
    args = sys.argv[1:]
    diary = Diary()

    if not args:
        diary.edit_entry()
    elif args[0] == "cat":
        diary.cat_entry()
    else:
        target_date = diary.parse_date(args[0])
        diary.edit_entry(target_date)