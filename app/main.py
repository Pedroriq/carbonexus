import os

from flask import Flask, render_template, request, Response

from flaskwebgui import FlaskUI
from loguru import logger
from measurement.github.github import Repository

import time
import threading
import logging
import sys

from utils.logger import StreamToLogger

if os.path.isfile('app/static/job.log'):
    os.remove('app/static/job.log')

logger = logging.getLogger('LOGs')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('app/static/job.log')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def flask_logger():
    with open("app/static/job.log", "r") as log_info:
        while True:
            sys.stdout = StreamToLogger(logger, logging.INFO)
            data = log_info.read()
            yield data.encode()
            time.sleep(1)


app = Flask(__name__)

ui = FlaskUI(app=app, server='flask')


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def gitclone():
    git_url = request.form.get('git-url')
    country = request.form.get('country')

    repository = Repository(git_url)

    git_thread = threading.Thread(target=repository.start)
    git_thread.start()

    return render_template('log.html')


@app.route('/log_stream', methods=['GET'])
def log_stream():
    return Response(flask_logger(), mimetype='text/plain', content_type='text/event-stream')


if __name__ == '__main__':
    # ui.run()
    app.run()
