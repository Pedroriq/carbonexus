from flask import Flask, render_template, request

from flaskwebgui import FlaskUI

from github import Repository

import threading

app = Flask(__name__)

ui = FlaskUI(app=app, server='flask')


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def gitclone():
    git_url = request.form.get('git-url')
    country = request.form.get('country')

    repository = Repository(git_url).start()
    # IMPLEMENTAR THREADS
    # git_thread = threading.Thread(target=repository.start())
    # git_thread.start()

    return render_template('log.html')


if __name__ == '__main__':
    ui.run()
    # app.run()

