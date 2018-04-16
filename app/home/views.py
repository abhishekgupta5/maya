#app/home/views.py
from flask import render_template

from . import home

@home.route('/')
def homepage():
    """
    Home page
    """
    return render_template('home/index.html')
