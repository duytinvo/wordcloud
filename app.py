# -*- coding: utf-8 -*-
"""
@author duytinvo
"""
import os
import csv
import argparse
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template, url_for, flash, redirect, send_file
from flask_cors import CORS
import signal
import datetime
import sys
import base64
from plot_wordcloud import WCBWC

IMG_FOLDER = os.path.join('static', 'images')
UPLOAD_FOLDER = os.path.join('static', 'texts')


# define the app
DebuggingOn = bool(os.getenv('DEBUG', False))  # Whether the Flask app is run in debugging mode, or not.
app = Flask(__name__)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'wcb'
CORS(app)  # needed for cross-domain requests, allow everything by default
app.config['IMG_FOLDER'] = IMG_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def sigterm_handler(_signo, _stack_frame):
    print(str(datetime.datetime.now()) + ': Received SIGTERM')


def sigint_handler(_signo, _stack_frame):
    print(str(datetime.datetime.now()) + ': Received SIGINT')
    sys.exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGINT, sigint_handler)


# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404


@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.route('/health')
def check_health():
    response = app.response_class(
        response="",
        status=200,
        mimetype='application/json')
    return response


@app.route('/')
def index():
    # return "<h1 style='color:blue'>Baseline Main Page</h1>"
    return render_template("index.html")


@app.route('/inference', methods=('GET', 'POST'))
def inference():
    if request.method == 'POST':
        if request.form.get("submit_a"):
            text = request.form['input']
            app.logger.info("DEBUG: " + str(len(text)))
            if len(text) == 0:
                flash('Either text or filename is required!')
            else:
                full_filename = os.path.join(app.config['IMG_FOLDER'], 'tmp.jpg')
                WCBWC.save_wc(text, full_filename)
                app.logger.info(request.form.get("submit_a"))
                return redirect("generate")

        if request.form.get("submit_b"):
            # check if the post request has the file part
            if 'file' not in request.files:
                print('no file')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                print('no filename')
                return redirect(request.url)
            else:
                # filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                text = file.read().decode('unicode_escape')
                full_filename = os.path.join(app.config['IMG_FOLDER'], 'tmp.jpg')
                WCBWC.save_wc(text, full_filename)
                app.logger.info(request.form.get("submit_b"))
                return redirect("generate")
    return render_template('inference.html')


@app.route('/generate', methods=('GET', 'POST'))
def generate():
    full_filename = os.path.join(app.config['IMG_FOLDER'], 'tmp.jpg')
    return render_template("generate.html", user_image=full_filename)
    # img_uri = base64.b64encode(open("./tmp.jpg", 'rb').read()).decode('utf-8')
    # return render_template("generate.html", img_uri=img_uri)


@app.route('/download', methods=('GET', 'POST'))
def download():
    full_filename = os.path.join(app.config['IMG_FOLDER'], 'tmp.jpg')
    return send_file(full_filename, as_attachment=True, cache_timeout=0)


@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("saved file successfully")
            # send file name as parameter to downlad
            return redirect('/downloadfile/'+ filename)
    return render_template('upload_file.html')


# Download API
@app.route("/downloadfile/<filename>", methods=['GET'])
def download_file(filename):
    return render_template('download.html', value=filename)


@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True, attachment_filename='')


if __name__ == '__main__':
    """
    kill -9 $(lsof -i:5000 -t) 2> /dev/null
    
    """
    app.run(debug=True)
    # app.run(host='0.0.0.0', debug=True)
