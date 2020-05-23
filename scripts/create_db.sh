#!/usr/bin/env bash

sqlite3 packages.db  <<END_SQL
CREATE TABLE IF NOT EXISTS binaries(
  name VARCHAR (20) PRIMARY KEY,
  version VARCHAR (20),
  source VARCHAR(20),
  maintainer VARCHAR(20),
  homepage VARCHAR(50),
  sha1 VARCHAR(100),
  sha256 VARCHAR(100),
  os_name VARCHAR(20),
  os_version VARCHAR(20),
  license VARCHAR(20),
  FOREIGN KEY (source) REFERENCES sources (name)
);
CREATE TABLE IF NOT EXISTS sources(
  name VARCHAR (20) PRIMARY KEY,
  version VARCHAR (20),
  binaries VARCHAR(1000),
  source_url VARCHAR(50),
  maintainer VARCHAR(20),
  homepage VARCHAR(50),
  sha1 VARCHAR(100),
  sha256 VARCHAR(100),
  pkg_zip VARCHAR(30),
  os_name VARCHAR(20),
  os_version VARCHAR(20),
  license VARCHAR(20)
);
END_SQL
