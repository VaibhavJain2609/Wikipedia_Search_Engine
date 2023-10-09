#!/usr/bin/env python3
"""maps word occurences."""
import sys

for line in sys.stdin:
    line = line.strip()
    text = line.split("\t")
    words = text[1].strip().split()
    for word in words:
        sys.stdout.write(f"{text[0]} {word}\t1\n")
