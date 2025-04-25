#!/bin/bash

FILE_URL="config.txt"

ENDPOINT="http://192.168.25.1:5000/guideDone"

curl -d @"$FILE_URL" "$ENDPOINT"