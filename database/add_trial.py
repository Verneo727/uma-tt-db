#!/usr/bin/env python3

import sqlite3

from setup.config import load_db_path

def add_trial_to_db(date: str, hour: str):
    try:
        db_path = load_db_path()
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        sql = "INSERT INTO Series (Serie_Date, Serie_Time) VALUES (?, ?)"
        cur.execute(sql, (date, hour))
        con.commit()
        con.close()
        return True, None
    except sqlite3.Error as e:
        return False, e