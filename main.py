import logging
import os
import queue
import sys
import threading
import time

from flask import Flask, Response, render_template, request
from flaskwebgui import FlaskUI
from loguru import logger

from app.measurement.pipeline.app import Pipeline
from app.utils.logger import StreamToLogger

if os.path.isfile("static/job.log"):
    os.remove("static/job.log")

logger = logging.getLogger("LOGs")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("static/job.log")
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

result_queue = queue.Queue()


def flask_logger():
    with open("static/job.log", "r") as log_info:
        while True:
            sys.stdout = StreamToLogger(logger, logging.INFO)
            data = log_info.read()
            yield data.encode()
            time.sleep(1)


app = Flask(__name__)

ui = FlaskUI(app=app, server="flask")


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def gitclone():
    git_url = request.form.get("git-url")
    country = request.form.get("country")

    git_thread = threading.Thread(
        target=Pipeline, args=(git_url, country, result_queue)
    )
    git_thread.start()

    return render_template("log.html")


@app.route("/log_stream", methods=["GET"])
def log_stream():
    return Response(
        flask_logger(), mimetype="text/plain", content_type="text/event-stream"
    )


@app.route("/results", methods=["GET"])
def results():
    result = result_queue.get()
    return render_template("results.html", result=result)


if __name__ == "__main__":
    # ui.run()
    app.run()
