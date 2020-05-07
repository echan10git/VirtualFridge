from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(64), index = True, unique = False)
    lastName = db.Column(db.String(64), index = True, unique = False)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    fridge = db.relationship('Fridge', lazy = 'dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Fridge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(140), index = True)
    quantity = db.Column(db.Integer, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def _repr_(self):
        return '<Fridge {}>'.format(self.ingredient)

