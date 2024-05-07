import math
import os
import re
import pathlib
from collections import Counter
import flask
import index

stop_words = []
pagerank = {}
inverted_index = {}

def cleanQuery(query):
    """Clean given query."""
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.casefold().split()
    query = [word for word in query if word not in stop_words]
    return query

def init():
    """Load inverted index, pagerank, and stopwords into memory."""
    index.app.config["INDEX_PATH"] = os.getenv(
        "INDEX_PATH", "inverted_index_1.txt"
    )

    index_dir = pathlib.Path(__file__).parent.parent

    """Read stopwords into memory."""
    path = index_dir / "stopwords.txt"
    with open(path, "r", encoding="utf-8") as file:
        global stop_words
        stop_words = set([line.strip() for line in file.readlines()])

    path = index_dir / "pagerank.out"
    # initialize the pagerank dict, {doc_id: pagerank score}
    with open(path, "r", encoding="utf-8") as file:
        global pagerank
        for line in file:
            line = line.replace("\n", "").split(",")
            pagerank[line[0]] = float(line[1])

    path = index_dir / "inverted_index" / index.app.config["INDEX_PATH"]
    with open(path, "r", encoding="utf-8") as file:
        # go over the whole file
        for line in file:
            line = line.split()
            word = line[0]
            idf_k = float(line[1])
            dictionaries = {}
            for i in range(2, len(line), 3):
                doc_id = line[i]
                tf_ik = float(line[i + 1])
                norm_factor = float(line[i + 2])
                dictionaries[doc_id] = {
                    "tf_ik": tf_ik,
                    "norm_factor": norm_factor
                }
            inverted_index[word] = {
                "idf_k": idf_k,
                "docs": dictionaries
            }

@index.app.route("/api/v1/", methods=["GET"])
def get_page():
    """Return all services of API."""
    services_dir = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**services_dir), 200


@index.app.route("/api/v1/hits/", methods=["GET"])
def get_hits():
    """Return hits from the provided query."""
    query = flask.request.args.get("q")
    pr_weight = float(flask.request.args.get("w", default=0.5))
    query = cleanQuery(query)
    all_docs = []
    for word in query:
        if word in inverted_index:
            all_docs.append(set(inverted_index[word]["docs"].keys()))
        else:
            return flask.jsonify(**{"hits": []}), 200
    if len(all_docs) == 0:
        return flask.jsonify(**{"hits": []}), 200
    docs = all_docs[0]
    for doc in all_docs:
        docs = docs.intersection(doc)

    hits = []
    for doc in docs:
        q_vect = []
        d_vect = []
        for word in query:
            q_vect.append(Counter(query)[word]*inverted_index[word]["idf_k"])
            d_vect.append(inverted_index[word]["docs"][doc]["tf_ik"]*inverted_index[word]["idf_k"])
            q_dot_d = sum(i[0] * i[1] for i in zip(q_vect, d_vect))
            norm_q = math.sqrt(sum(q**2 for q in q_vect))
            norm_d = math.sqrt(inverted_index[word]["docs"][doc]["norm_factor"])
            tfidf = (q_dot_d / (norm_q * norm_d))
        hits.append({
            "docid": int(doc),
            "score": pr_weight*pagerank[doc] + (1 - pr_weight)*tfidf
        })
    output = {
        "hits": sorted(hits, key=lambda x: x["score"], reverse=True)
    }
    return flask.jsonify(**output), 200