#app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login_manager

class User(UserMixin, db.Model):
    '''
    Table for users.
    '''
    __tablename__ = 'users'

    #Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

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

#Setting up user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
