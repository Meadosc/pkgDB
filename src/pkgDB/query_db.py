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


def select_source_url(conn=None):
    """select source URL, binary package name."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT binaries.name, source_url FROM binaries INNER JOIN sources WHERE binaries.name=sources.name """
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
        return None
    return cursor.fetchall()


if __name__ == "__main__":
    conn = create_connection(db_file="./data/db/packages.db")
    pkg_list = []
    for row in select_source_url(conn):
        pkg_list.append({"binary": row[0], "url": row[1]})
    with open("./data/json/apt_pkg_source_url.json", "w") as fh:
        json.dump(pkg_list, fh)

