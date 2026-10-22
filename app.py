import os

from flask import Flask, render_template

app = Flask(__name__)


@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, max-age=0"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return "", 204


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host=host, port=port, debug=debug)
