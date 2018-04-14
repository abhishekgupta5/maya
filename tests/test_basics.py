#tests/tests_basics.py

import unittest
from flask import current_app
from app import create_app, db

class BasicTestCase(unittest.TestCase):
    #setUp and teardown will be called before and after each test respectively
    def setUp(self):
        #Create app and configure it for testing
        self.app = create_app('testing')
        #Activate app's context
        self.app_context = self.app.app_context()
        self.app_context.push()
        #Populate the testing db
        db.create_all()

    def tearDown(self):
        #Remove db and app context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
