from flask import Flask, request, jsonify, render_template, url_for
from logging.handlers import RotatingFileHandler
from time import strftime

from model.model import Square

import logging
import traceback

app = Flask(__name__)

@app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        logger.error('%s %s %s %s %s',
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      response.status)
    return response

@app.errorhandler(Exception)
def exception(e):
    """ Logging after every Exception. """
    logger.error('%s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  tb)
    return "Internal Server Error", 500

@app.route('/create', methods=['POST'])
def create():
    logger.info('Creating a new square')
    square = Square(int(request.form['side']))
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes= 1024 * 1024, backupCount= 5)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    app.run(host='127.0.0.1', port=8000, debug=True)
 