#!/usr/bin/env bash

from multiprocessing import Process
import re
import sqlite3
import json

import ray
import requests
import tqdm

from bs4 import BeautifulSoup as BS


def create_connection(db_file):
    """create db connection to db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn


def select(items, table=None, conn=None):
    """select from table items."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT {} from {};".format(items, table))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
        return None
    return cursor.fetchall()


def fetch_alpine_lc_file(pkg):
    """check alpinelinux for licenses of pkgs."""
    orig_url = "https://pkgs.alpinelinux.org/packages?name={}&branch=edge"
    url = orig_url.format(pkg)
    pkg_src = requests.get(url).text
    license = BS(pkg_src, features="lxml").find("td", attrs={"class": "license"})
    if not license:
        url = orig_url.format(re.compile(r"_|-").split(pkg)[0])
        pkg_src = requests.get(url).text
        license = BS(pkg_src, features="lxml").find("td", attrs={"class": "license"})
    if license:
        license = license.text
    else:
        license = ""
    return license


def fetch_arch_lc_file(pkg):
    """check alpinelinux for licenses of pkgs."""
    orig_url = "https://www.archlinux.org/packages/community/x86_64/{}/"
    url = orig_url.format(pkg)
    pkg_src = requests.get(url).text
    # print("tyring url: {}".format(url))
    try:
        license = BS(pkg_src, features="lxml").find_all("td", attrs={"class": "warp"})[
            1
        ]
        if license:
            license = license.text
        else:
            license = ""
    except IndexError:
        # print("no license in arch repo")
        license = ""
    return license


def fetch_license_file(rows, saveto=None):
    pkg_license = {}
    for pkg in rows:
        pkg = pkg[0]
        lc = fetch_alpine_lc_file(pkg)
        if not lc:
            lc = fetch_arch_lc_file(pkg)
        # print("lc of :",pkg,"=", lc)
        pkg_license[pkg] = lc
    with open(saveto, "w") as fh:
        json.dump(pkg_license, fh)


@ray.remote
def sources():
    conn = create_connection("./packages.db")
    items = "name"
    table = "binaries"
    rows = select(items, table, conn)
    fetch_license_file(rows, saveto="{}-pkg-licenses.json".format(table))
    return True


@ray.remote
def binaries():
    conn = create_connection("./packages.db")
    items = "name"
    table = "sources"
    rows = select(items, table, conn)
    fetch_license_file(rows, saveto="{}-pkg-licenses.json".format(table))
    return True


if __name__ == "__main__":
    # p1 = Process(target = sources)
    # p1.start()
    # p2 = Process(target = binaries)
    # p2.start()
    ray.init()
    srcs, bics = sources.remote(), binaries.remote()
    s, b = ray.get([srcs, bics])
    print("sources process: {}", s)
    print("binaries process: {}", b)
