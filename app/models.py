from virtualfridge import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from virtualfridge import login

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    fridges = db.relationship('Fridge')
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Fridge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(140))
    quantity = db.Column(db.Integer, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Fridge {}>'.format(self.ingredient)

