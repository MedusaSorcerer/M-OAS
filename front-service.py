#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
from flask import Flask, render_template

app = Flask(__name__, template_folder=r'./front', static_folder='./front', static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8088
    debug = False
    app.run(debug=debug, host=host, port=port)
