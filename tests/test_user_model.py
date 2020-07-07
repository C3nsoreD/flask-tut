import unittest
from app.models import User 
from app import db


class UserModelTestCase(unittest.TestCase):
    
    def test_password_setter(self):
        u = User(password='hello')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='hello')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='hello')
        self.assertTrue(u.verify_password('hello'))
        
        self.assertFalse(u.verify_password('Hello'))

    def test_password_salts_are_random(self):
        u = User(password='hello')
        u2 = User(password='hello')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password='cat')
        u2 = User(password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))
       