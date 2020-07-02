from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    api_key = db.Column(db.String(120), index=True, unique=True)
    url_api_key = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, nick, api_key, url_api_key, password):
        self.nick = nick
        self.api_key = api_key
        self.url_api_key = url_api_key
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
