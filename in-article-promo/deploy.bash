#!/bin/bash
python ingest.py http://www.denverpost.com/dont-miss/feed/
../ftp.bash --dir $REMOTE_DIR --host $REMOTE_HOST
