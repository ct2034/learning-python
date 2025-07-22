#!/usr/bin/bash

# look at some params ...
# fandango fuzz -f strings.fan -n 3

# fuzz our code ...
fandango fuzz -f strings.fan -n 10 --input-method=stdin ./device_under_test.py
