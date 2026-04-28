#!/usr/bin/env python3

import sqlite3
import configparser
import sys
import shutil

from pathlib import Path
from setup.config import load_db_path
from setup.resources import resource_path

def pragma(app_path):
    DB_PATH = load_db_path(app_path)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("PRAGMA user_version")
    version = cur.fetchone()[0]
    con.close()
    return version

def create_db(app_path):
    SQL = resource_path(f'uma-tt-db/assets/tt.sql')
    SQL2 = resource_path(f'uma-tt-db/assets/tt_2.sql')
    sql_script = Path(SQL).read_text(encoding="utf-8")
    sql2_script = Path(SQL2).read_text(encoding="utf-8")

    db_path = Path(app_path)/"uma.db"
    db_path.touch()

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("PRAGMA user_version")
    version = cur.fetchone()
    version = version[0] if version else 0

    if version == 0:
        cur.executescript(sql_script)
        cur.execute("PRAGMA user_version = 1")
        version = 1
        print("Database initialized to version 1.")

    if version == 1:
        backup_path = f"{db_path}.backup"
        try:
            shutil.copy2(db_path, backup_path)
        except Exception as e:
            print(f"Error during creating database backup file:\n{e}")
            print(">> Please contact with developer.")
            sys.exit(1)
        cur.executescript(sql2_script)
        cur.execute("PRAGMA user_version = 2")
        version = 2
        print("Database initialized to version 2.")

    # Protection against database incompatibility.
    # Database sourced from a newer version of the program.
    # !Must be updated when the database version changes.
    # !Actual: 2
    if version > 2:
        print("The database is too new!\n>Please, update the program!")
        con.close()
        sys.exit(1)

    con.commit()
    con.close()
    db_path_update(app_path)

def db_path_update(app_path):
    config_file = Path(app_path)/"config.ini"
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")
    if 'APP' not in config:
        config['APP'] = {}

    config['APP']['database'] = str(app_path/"uma.db")
    with open(config_file, "w", encoding="utf-8") as f:
        config.write(f)