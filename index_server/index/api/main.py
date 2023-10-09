"""api request methods."""
from pathlib import Path
from collections import defaultdict
import math
import re
import os
import flask
import index

SW = set()
PR = {}


def init():
    """Initialize the inverted index."""
    index.app.config["INDEX_PATH"] = os.getenv(
        "INDEX_PATH", "inverted_index_1.txt"
    )

    with open(
        "index_server/index/stopwords.txt", "r", encoding="UTF-8"
    ) as file:
        global SW
        SW = set([line.strip() for line in file.readlines()])

    with open(
        "index_server/index/pagerank.out", "r", encoding="UTF-8"
    ) as file:
        global PR
        lines = file.readlines()
        for line in lines:
            line = line.split(",")
            line = [word.strip() for word in line]
            PR[int(line[0])] = float(line[1])


@index.app.route("/api/v1/", methods=["GET"])
def get_page():
    """Get the page."""
    context = {"hits": "/api/v1/hits", "url": "/api/v1/"}
    return flask.jsonify(**context), 200


@index.app.route("/api/v1/hits/", methods=["GET"])
def get_hits():
    """Get hits for a query."""
    q_res = flask.request.args.get("q", default="", type=str)
    w_res = flask.request.args.get("w", default=0.5, type=float)

    # clean query
    q_res = q_res.split()
    q_res = [re.sub(r"[^a-zA-Z0-9]+", "", word.strip()) for word in q_res]
    q_res = [word.lower() for word in q_res]
    q_res = [word for word in q_res if word not in SW]
    print(q_res)

    # Initialize an empty dictionary to store the data
    term_dict = {}
    # Define the path to the file
    file_path = Path("index_server/index/inverted_index") / Path(index.app.config["INDEX_PATH"])
    # Open the file in read mode with UTF-8 encoding
    with open(file_path, "r", encoding="UTF-8") as file:
        # Read all lines from the file
        lines = file.readlines()
        # Cleaning the inquires
        for line in lines:
            words = line.split()
            cleaned_words = [word.strip() for word in words]
            term = cleaned_words[0]
            weight = float(cleaned_words[1])
            data = cleaned_words[2:]
            term_dict[term] = (weight, data)
    potential_docs = defaultdict(set)
    # Iterate through words in q_res
    for word in q_res:
        # Check if the word is in the term_dict
        if word in term_dict:

            potential_docs[word].update({int(val) for idx, val in enumerate(term_dict[word][1]) if idx % 3 == 0})
        else:
            potential_docs[word] = set()

    docs = set.intersection(*[potential_docs[key] for key in potential_docs])

    # calculating the query vector
    query = [term_dict[word][0] * len(docs) if word in term_dict else 0 for word in q_res]

    doc_dict = defaultdict(list)
    for doc in docs:
        for word in q_res:
            if word in term_dict:
                for idx, val in enumerate(term_dict[word][1]):
                    if idx % 3 == 0 and int(val) == doc:
                        freq = int(term_dict[word][1][idx + 1])
                        norm_score = float(term_dict[word][1][idx + 2])
                        score = freq * term_dict[word][0]
                        doc_dict[(doc, norm_score)].append(score)
            else:
                doc_dict[(doc, 0)].append(0)

    # Dot product of  query vector and  document vector
    scores_dict = {}
    for doc in doc_dict:
        score = sum([a * b for a, b in zip(query, doc_dict[doc])])
        scores_dict[doc] = score

    query_norm = sum([x**2 for x in query]) ** 0.5

    pr_score = {}
    for doc in doc_dict:
        doc_id = doc[0]
        tf_idf = scores_dict[doc] / (query_norm * math.sqrt(float(doc[1])))
        weight = w_res * PR[doc_id] + (1 - w_res) * tf_idf
        pr_score[doc_id] = weight

    context = {"hits": []}
    # Sort pr_score by values in descending order and create a new dictionary with sorted key-value pairs
    pr_score = dict(sorted(pr_score.items(), key=lambda item: item[1], reverse=True))

    for doc in pr_score:
        context["hits"].append({"docid": doc, "score": pr_score[doc]})

    return flask.jsonify(**context), 200
