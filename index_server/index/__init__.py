"""initialization file for the package."""
import flask

app = flask.Flask(__name__)

# Load inverted index, stopwords, and pagerank into memory
import index.api  # noqa: E402  pylint: disable=wrong-import-position

index.api.init()
