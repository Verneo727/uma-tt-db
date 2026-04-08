#!/usr/bin/env python3

__author__ = "Mateusz Jamróz"
__app_name__ = "UmaTT_DB"

import tkinter as tk
import argparse
import subprocess

from gui.window.main_window import MainWindow
from setup.os_check import check_os
from setup.folders_mng import create_folders
from setup.config import create_config
from setup.json import create_json
from setup.lang import lang_check
from database.db_manager import create_db
from metadata import __version__

def update():
    """Update the program from the Github repository and exit."""
    print("Checking for updates...")
    try:
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
        output = result.stdout.strip()
        if 'up to date' in output.lower() or 'aktualne' in output.lower():
            print("The program is already up to date :)")
        else:
            print("Update successful!")
            print(result.stdout)
    except FileNotFoundError:
        print("Error: Git is not installed or not found in PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")

def version():
    """Show the program version and exit."""
    print(f"{__version__}")

def start():
    """Initialize the environment and launch the main application interface."""
    system = check_os()
    app_path = create_folders(system, __app_name__)
    create_config(app_path)
    create_db(app_path)
    create_json(app_path)
    lang = lang_check(app_path)
    root = tk.Tk()
    root.withdraw()
    MainWindow(app_path, lang, __app_name__, master=root)
    root.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=f"{__app_name__}")
    parser.add_argument(
        "-U", "--update",
        action="store_true",
        help="Update the program using git pull"
    )
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Show version."
    )
    args = parser.parse_args()
    if args.update:
        update()
    elif args.version:
        version()
    else:
        start()