#!/usr/bin/env python3
"""maps docid to doc metadata."""
import sys

for line in sys.stdin:
    line = line.strip()
    text = line.split("\t")
    t_k = text[0].strip()
    d_id = text[1].split()[0].strip()
    tf_k = text[1].split()[1].strip()
    idf_k = text[1].split()[2].strip()
    sys.stdout.write(f"{d_id}\t{t_k} {tf_k} {idf_k}\n")
