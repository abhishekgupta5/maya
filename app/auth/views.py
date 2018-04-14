#app/auth/views.py

from flask import render_template
from . import auth

@auth.route('/login')
def login():
    return 'This is login route in auth blueprint'
