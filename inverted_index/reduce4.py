#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    key = key.strip()
    norm = 0.0
    output_list = []

    for term in group:
        term_parts = term.strip().split("\t")
        d_id, t_k, tf_k, idf_k = map(str.strip, term_parts[0].split() + term_parts[1].split())
        norm += (float(tf_k) * float(idf_k)) ** 2
        output_list.append(f"{t_k} {tf_k} {idf_k}")

    sys.stdout.write(f"{d_id}\t{output_list} {norm}\n")

def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
