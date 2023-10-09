"""main.py."""

from search.config import SEARCH_INDEX_SEGMENT_API_URLS
import flask
import search
import search.model
import requests

import heapq
import time

import threading


@search.app.route('/')
def show_index():
    """Display / route."""
    # Get the search query from the URL
    query = flask.request.args.get('q')
    weight = flask.request.args.get('w', default=0.5)

    context = {
        "show_search": True,
        "search_results": [],
        "query": query if query else "",
        "weight": weight,
    }
    if query is None or weight is None:
        context["show_search"] = False
        return flask.render_template("index.html", **context)

    # Recieve search results
    urls = search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]
    search_results = []
    threads = []
    for url in urls:
        thread = threading.Thread(target=search_index_segment,
                                  args=(query, weight, url, search_results))
        threads.append(thread)
        thread.start()
    while threads[0].is_alive() or threads[1].is_alive() or threads[2].is_alive():
        time.sleep(0.1)
    connection = search.model.get_db()
    for search_result in heapq.merge(*search_results,
                                     key=lambda x: x["score"],
                                     reverse=True):
        cur = connection.execute(
            "SELECT * FROM Documents WHERE docid = ?",
            (search_result["docid"],)
        )
        document = cur.fetchone()
        if len(context["search_results"]) < 10:
            context["search_results"].append({
                "doc_url": document["url"],
                "doc_title": document["title"],
                "doc_summary": document["summary"],
            })
    return flask.render_template("index.html", **context)


def search_index_segment(query, weight, url, search_results):
    """Search index segment."""
    # Construct the search URL
    search_url = f"{url}?q={query}&w={weight}"
    # Get the search results
    response = requests.get(search_url)
    if response:
        search_results.append(response.json()["hits"])
