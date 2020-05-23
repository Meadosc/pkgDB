#!/usr/bin/env bash

OS=ubuntu
VERSION=focal
URL=http://archive.ubuntu.com
REPO=main
TYPE=binary-amd64
NAME=Packages.gz
FNAME=pkgs.txt.gz

wget "$URL/$OS/dists/$VERSION/$REPO/$TYPE/$NAME" -O "$FNAME"

if [[ -f $FNAME ]]; then
  gunzip -d $FNAME
fi

TYPE=source
NAME=Sources.gz
FNAME=sources.txt.gz
wget "$URL/$OS/dists/$VERSION/$REPO/$TYPE/$NAME" -O "$FNAME"

if [[ -f $FNAME ]]; then
  gunzip -d $FNAME
fi
