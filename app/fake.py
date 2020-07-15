from random import randint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from faker import Faker
from . import db
from .models import User, Post

def user(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                username=fake.user_name(),
                password='password',
                confirmed=True,
                name=fake.name(),
                location = fake.city(),
                about_me = fake.text(),
                member_since=fake.past_date())
        db.session.add(u)
        # Try to commit changes
        # In case of any duplicates raise an IntegrityError
        try:
            db.session.commit()
            i += 1
        except exc.IntegrityError:
            db.session.rollback()


def post(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(),
                timestamp=fake.past_date(),
                author=u
                )
        db.session.add(p)
    db.session.commit()
