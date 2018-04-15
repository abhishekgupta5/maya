#tests/test_user_model.py
import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    '''
    Tests for User model
    '''
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

