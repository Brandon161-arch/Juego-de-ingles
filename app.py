import os
import secrets

from flask import Flask, Response, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
GAME_HTML = "index.html"

APP_ENV = os.environ.get("APP_ENV", "production").strip().lower()
DEBUG = os.environ.get("FLASK_DEBUG", "1" if APP_ENV != "production" else "0") == "1"

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config.update(
    ENV=APP_ENV,
    DEBUG=DEBUG,
    TEMPLATES_AUTO_RELOAD=DEBUG,
    SEND_FILE_MAX_AGE_DEFAULT=0,
)


@app.after_request
def security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
    return response


@app.route("/")
def index():
    response = send_from_directory(TEMPLATES_DIR, GAME_HTML, conditional=True)
    response.headers["Cache-Control"] = "no-cache, must-revalidate"
    return response


@app.route("/healthz")
def healthz():
    return {"status": "ok", "app": "robo-runner", "env": APP_ENV}


@app.route("/favicon.ico")
def favicon():
    return Response(status=204)


@app.errorhandler(404)
def not_found(_error):
    return Response("No encontrado", status=404, mimetype="text/plain")


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port, debug=DEBUG)
