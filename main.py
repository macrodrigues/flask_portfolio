"""This script launches the Flask server and renders the portfolio page."""
# pylint: disable=E0401
from flask import Flask, render_template
from flask_compress import Compress
import os
import datetime as dt

OWN_EMAIL = os.getenv('mail')
OWN_PASSWORD = os.getenv('pass')


app = Flask(__name__)
compress = Compress()
compress.init_app(app)


@app.route("/")
def home():
    """Render index.html template."""
    current_year = dt.datetime.now().year
    return render_template('index.html', year=current_year)


@app.route("/skills")
def skills():
    """Render index.html template and scroll to skills section."""
    current_year = dt.datetime.now().year
    return render_template('index.html', year=current_year, scroll_to='skills')


@app.route("/projects")
def projects():
    """Render index.html template and scroll to projects section."""
    current_year = dt.datetime.now().year
    return render_template('index.html', year=current_year, scroll_to='projects')


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=5000, host='0.0.0.0', debug=True)
