#app/models.py

from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    '''
    Table for users.
    '''
    __tablename__ = 'users'

    #Columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True, index=True)
    #Temporary storing passwords without hashing
    password_plain = db.Column(db.String(128), nullable=False)

    def __init__(self, email, password_plain):
        self.email = email
        self.password_plain = password_plain

    def __repr__(self):
        return '<User {0}>'.format(self.name)

