from app import accountdb
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, accountdb.model):
    id = accountdb.Column(accountdb.Integer, primary_key = True)
    firstName = accountdb.Column(accountdb.String(64), index = True, unique = False)
    lastName = accountdb.Column(accountdb.String(64), index = True, unique = False)
    username = accountdb.Column(accountdb.String(64), index = True, unique = True)
    password = accountdb.Column(accountdb.String(120), index = True, unique = True)
    email = accountdb.Column(accountdb.String(120), index = True, unique = True)
    password_hash = accountdb.Column(accountdb.String(128))
    fridge = accountdb.relationship('Fridge', lazy = 'dynamic')
    def _repr_(self):
        return '<User {}>'.format(self.username)
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Fridge(accountdb.model):
    id = accountdb.Column(accountdb.String(140))
    ingredient = accountdb.Column(accountdb.String(140), index = True)
    quantity = accountdb.Column(accountdb.Integer, index = true)
    user_id = accountdb.Column(accountdb.Integer, accountdb.ForeignKey('user.id'))
    def _repr_(self):
        return '<Fridge {}>'.format(self.ingredient)

