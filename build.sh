#!/bin/bash

ZIP=slosint-retoure-python.zip

if test -f "$ZIP"; then
  rm "$ZIP"
fi

cd venv/lib/python3.8/site-packages
zip -x=*__pycache__* -r9 ../../../../"$ZIP" xlrd
cd -

cd src
zip -r9 ../"$ZIP" .
