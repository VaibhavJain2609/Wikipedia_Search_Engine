#!/usr/bin/env python3
"""Template reducer."""
import sys
import itertools
import re


def reduce_one_group(key, group):
    group = [file.strip().split("\t") for file in group]
    output = {}
    key = key.strip()

    for _, d_id, file_text in group:
        l_o_t = file_text[:file_text.index("]") + 1].replace("[", "").replace("]", "").split(",")
        norm = file_text[file_text.index("]") + 2:].strip()

        for text in l_o_t:
            t_k, tf_k, idf_k = text.strip().replace("[", "").replace("]", "").replace("'", "").split()
            if t_k not in output:
                output[t_k] = f"{idf_k} {d_id} {tf_k} {norm}"
            else:
                output[t_k] += f" {d_id} {tf_k} {norm}"

    output = sorted(output.items(), key=lambda x: x[0])

    for term, line in output:
        term, line = re.sub(r"\s+", " ", term), re.sub(r"\s+", " ", line)
        sys.stdout.write(f"{term} {line}\n")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
