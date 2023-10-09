#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys

for line in sys.stdin:
    sys.stdout.write(f"{line.strip()}\n")
