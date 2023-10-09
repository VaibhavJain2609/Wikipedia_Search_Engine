#!/usr/bin/env python3
"""maps term to docid and freq."""
import sys

for line in sys.stdin:
    line = line.strip()
    text = line.split("\t")
    t_k = text[0].split()[1].strip()
    freq = text[1].strip()
    d_id = text[0].split()[0].strip()
    sys.stdout.write(f"{t_k}\t{d_id} {freq}\n")
