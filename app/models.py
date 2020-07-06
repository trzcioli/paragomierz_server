from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


class User(db.Model):
    email = db.Column(db.String(120), index=True,
                      unique=True, primary_key=True)
    api_key = db.Column(db.String(500), index=True, unique=True)
    url_api_key = db.Column(db.String(500), index=True, unique=True)
    password = db.Column(db.String(128))

    def __init__(self, email, api_key, url_api_key, password):
        self.email = email
        self.api_key = api_key
        self.url_api_key = url_api_key
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def generate_auth_token(self, expiration=60 * 60 * 24):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'email': self.email})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return User.query.get(data['email'])

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)
