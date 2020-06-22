#!/usr/bin/env python

import json
import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn


def update(value, condition, table=None, conn=None):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE {} SET license = ? WHERE name = ? """.format(table),
            (value, condition),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
        return None
    return cursor.lastrowid


if __name__ == "__main__":
    conn = create_connection(db_file="./data/db/packages.db")
    with open("./data/json/sources-pkg-licenses.json", "r") as fh:
        data = json.load(fh)
        table = "sources"
        for name, lc in data.items():
            update(lc, name, table, conn)

    with open("./data/json/binaries-pkg-licenses.json", "r") as fh:
        data = json.load(fh)
        table = "binaries"
        for name, lc in data.items():
            update(lc, name, table, conn)
