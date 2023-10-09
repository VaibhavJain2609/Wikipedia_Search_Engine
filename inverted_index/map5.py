#!/usr/bin/env python3
"""maps doc mod idx to doc body."""
import sys

for line in sys.stdin:
    line = line.strip()
    text = line.split("\t")
    d_id = text[0].strip()
    INDEX = int(float(d_id)) % 3
    sys.stdout.write(f"{INDEX}\t{line}\n")
