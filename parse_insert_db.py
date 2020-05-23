#!/usr/bin/env python

import itertools
import sqlite3


def blocks(line):
    return line == "\n"


def parse_meta(filename=None):
    fproto = ["http", "https",  "ftp", "smtp"]
    with open(filename, "r") as fh:
        for key, group in itertools.groupby(fh, blocks):
            if not key:
                block = {}
                for item in group:
                    field, *value = item.split(":", 1)
                    value = ":".join(value).strip()
                    block[field] = value
            yield block


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn


def insert(items, table=None, conn=None):
    entries = "?," * len(items)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO {0} values ({1})".format(table, entries[:-1]), items
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
        return None
    return cursor.lastrowid

def parse_src_sha(keys):
    ky = []
    for k in keys:
        if k.endswith("tar.xz\n"):
            ky.append(k)
    print(ky)
    try:
        sha1 = ky[1].split(" ")[1]
    except IndexError:
        sha1 = ""
    try:
        sha256 = ky[2].split(" ")[1]
    except IndexError:
        sha256 = ""
    try:
        tar_file = ky[2].split(" ")[3]
    except IndexError:
        tar_file = ""
    return sha1, sha256, tar_file



if __name__ == "__main__":
    conn = create_connection(db_file="packages.db")
    for block in parse_meta("./sources.txt"):
        keys = block.keys()
        sha1, sha256, tar_file = parse_src_sha(keys)
        sources_items = [
            block["Package"],
            block["Version"],
            block.get("Binary", ""),
            block.get("Vcs-Browser", ""),
            block.get("Maintainer", ""),
            block.get("Homepage", ""),
            sha1, sha256, tar_file,
            "ubuntu",
            "focal",
            "",
        ]
        insert(sources_items, table="sources", conn=conn)
 
    """for block in parse_meta("./pkgs.txt"):
        binaries_items = [
            block["Package"],
            block["Version"],
            block.get("Source", block["Package"]),
            block.get("Maintainer", ""),
            block.get("Homepage", ""),
            block["SHA1"],
            block["SHA256"],
            "ubuntu",
            "focal",
            "",
        ]
        insert(binaries_items, table="binaries", conn=conn)
    """
