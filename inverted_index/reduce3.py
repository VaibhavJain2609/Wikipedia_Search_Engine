#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math


def reduce_one_group(key, group):
    """Reduce one group."""
    file_count = 0
    with open("total_document_count.txt", "r", encoding='UTF-8') as file:
        file_count = float(file.readline())

    group = list(group)
    for doc in group:
        doc = doc.strip().split()
        t_k = doc[0].strip()
        d_id = doc[1].strip()
        tf_k = doc[2].strip()
        idf_k = math.log10(file_count / len(list(group)))
        key = key.strip()
        sys.stdout.write(f"{t_k}\t{d_id} {tf_k} {idf_k}\n")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
