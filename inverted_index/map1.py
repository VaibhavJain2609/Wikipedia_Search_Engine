#!/usr/bin/env python3
"""maps document id to document body."""
import sys
import csv
import re

csv.field_size_limit(sys.maxsize)
for line in csv.reader(sys.stdin):
    line = [re.sub(r"[^a-zA-Z0-9 ]+", "", word) for word in line]
    doc_id = line[0].strip()
    TITLE_BODY = line[1] + " " + line[2]
    stopwords = set()
    with open("stopwords.txt", "r", encoding='UTF-8') as f:
        for line in f:
            stopwords.add(line.strip())
    TITLE_BODY = TITLE_BODY.casefold().split()
    TITLE_BODY = [
        word.strip() for word in TITLE_BODY if word.strip() not in stopwords
    ]
    TITLE_BODY = " ".join(TITLE_BODY)
    sys.stdout.write(f"{doc_id}\t{TITLE_BODY}\n")
