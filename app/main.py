from flask import Flask, render_template, request, Response

from flaskwebgui import FlaskUI
from loguru import logger
from github import Repository

import datetime, time

logger.add("app/static/job.log", format="{time} - {message}")


def flask_logger():
    with open("app/static/job.log", "r") as log_info:
        for i in range(25):
            logger.info(f"iterarion {i}")
            data = log_info.read()
            yield data.encode()
            time.sleep(1)

        log_info.close()


app = Flask(__name__)

ui = FlaskUI(app=app, server='flask')


@app.route('/')
def index_page():
    return render_template('log.html')


@app.route('/submit', methods=['GET', 'POST'])
def gitclone():
    # git_url = request.form.get('git-url')
    # country = request.form.get('country')
    #
    # repository = Repository(git_url).start()
    # IMPLEMENTAR THREADS
    # git_thread = threading.Thread(target=repository.start())
    # git_thread.start()

    return render_template('log.html')


@app.route('/log_stream', methods=['GET'])
def log_stream():
    return Response(flask_logger(), mimetype='text/plain', content_type='text/event-stream')


if __name__ == '__main__':
    # ui.run()
    app.run()
