#tests/test_user_model.py
import unittest
import time
from app import create_app, db
from app.models import User

class UserModelTestCase(unittest.TestCase):
    '''
    Tests for User model
    '''
    def setUp(self):
        #Create an app and configure it for testing
        self.app = create_app('testing')
        #Activate app's context
        self.app_context = self.app.app_context()
        self.app_context.push()
        #populate the testing db
        db.create_all()

    def tearDown(self):
        #Remove db and app context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='abcde')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='bacde')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='asd')
        self.assertTrue(u.verify_password('asd'))
        self.assertFalse(u.verify_password('ase'))

    def test_password_salts_are_random(self):
        u1 = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u1.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password='abc')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password="abc")
        u2 = User(password="def")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password="xyz")
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))
