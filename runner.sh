#!/usr/bin/env bash

for i in /srv/nbgrader/exchange/data_science/outbound/* ; do
  if [ -d "$i" ]; then
    base=$(basename "$i")
    echo "About to do autograding for: $base"
    python3 /home/instructor/nbgrader-autograde-container/test_code.py "$base"
  fi
done