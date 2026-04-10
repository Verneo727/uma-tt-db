#!/usr/bin/env python3

import sqlite3

from setup.config import load_db_path

def load_umas(app_path):
    """Retrieve Uma's ID, name and rank."""
    db_path = load_db_path(app_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT Uma_ID, Uma_Name, Uma_Rank FROM Uma")
    rows = cur.fetchall()
    con.close()
    return rows

def load_umas_by_id(uma_ids, app_path):
    """Retrieve Uma's ID, name, rank and distance."""
    db_path = load_db_path(app_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    if not uma_ids:
        return {}
    placeholders = ",".join("?" for _ in uma_ids)
    sql = f"""
    SELECT Uma_ID, Uma_Name, Uma_Rank, Distance_ID
    FROM Uma
    WHERE Uma_ID IN ({placeholders})
    """
    cur.execute(sql, uma_ids)
    return {
        row[0]: {
            "name": row[1],
            "rating": row[2],
            "distance": row[3],
        }
        for row in cur.fetchall()
    }

def load_uma_position(uma_id, app_path):
    """
    Retrieve Uma's race positions and timestamps by her ID.
    Results are sorted chronologically.
    """
    db_path = load_db_path(app_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    sql = """
    SELECT t.Trial_Date, t.Trial_Time, r.Position
    FROM Results r
    JOIN Trials t ON r.Trial_ID = t.Trial_ID
    WHERE r.Uma_ID = ?
    ORDER BY t.Trial_Date ASC, t.Trial_Time ASC
    """
    cur.execute(sql, (uma_id,))
    rows = cur.fetchall()
    con.close()
    labels = [f"{row[0]} {row[1]}" for row in rows]
    positions = [row[2] for row in rows]

    return labels, positions

def load_uma_name(uma_id, app_path):
    """Retrieve Uma's name by her ID."""
    db_path = load_db_path(app_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(f"SELECT Uma_Name FROM Uma WHERE Uma_ID = {uma_id}")
    name = cur.fetchall()
    con.close()
    if isinstance(name, (list, tuple)):
        name = name[0][0]
        return name
    else:
        return name

def load_umas_by_distance(distance_id, app_path):
    """Retrieve all Umas for a given distance."""
    db_path = load_db_path(app_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql = "SELECT Uma_ID FROM Uma WHERE Distance_ID = ?"
    cur.execute(sql, (distance_id,))
    umas = cur.fetchall()
    con.close()
    return umas

def load_umas_by_trial(serie_id, app_path):
    """Retrieve all Umas for a given TT race."""
    db_path = load_db_path(app_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql = """
    SELECT Uma.Uma_ID FROM Uma
    JOIN Results on Uma.Uma_ID = Results.Uma_ID
    WHERE Results.Trial_ID = ?
    """
    cur.execute(sql, (serie_id,))
    umas = cur.fetchall()
    con.close()
    return umas

def load_uma_result_in_trial(uma_id, trial_id, app_path):
    """Retrieve all Uma results and distances for a given TT race."""
    db_path = load_db_path(app_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql = f"""
    SELECT Position, Distance_ID
    FROM Results
    WHERE Uma_ID = {uma_id}
    AND Trial_ID = {trial_id}
    """
    cur.execute(sql)
    res = cur.fetchone()
    con.close

    if res:
        return res[0], res[1]
    return 0, 0