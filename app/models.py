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
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        '''Prevent password from being accessed'''
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        '''Set password hash'''
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        '''Verify password hash'''
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {0}>'.format(self.email)

