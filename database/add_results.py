#!/usr/bin/env python3

import sqlite3

from setup.config import load_db_path

def add_results_to_db(inputs_to_db, app_path):
    db_path = load_db_path(app_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    sql = """
        INSERT INTO Results (Trial_ID, Uma_ID, Position, Score, Distance_ID)
        VALUES (?, ?, ?, ?, ?)
        """
    cur.executemany(sql, inputs_to_db)
    con.commit()
    con.close()