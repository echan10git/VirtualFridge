from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, db
from hashlib import md5

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    about_me = db.Column(db.String(140))
    password_hash = db.Column(db.String(128))
    fridge = db.relationship('Fridges', backref='author', lazy = 'dynamic')
    recipe = db.relationship('Recipes', backref='author', lazy = 'dynamic')
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Fridges(db.Model):
    __tablename__ = 'fridges'
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(140), index = True)
    quantity = db.Column(db.Integer, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def _repr_(self):
        return '<Fridges {}>'.format(self.ingredient)

class Recipes(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    likes = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    RecipeIngredient = db.relationship('RecipeIngredients', lazy = 'dynamic')
    def showingredients(self):
        return self.query.join(link, (self.id == RecipeIngredients.recipe_id)).filter(
            Link.c.recipeingredients_id == RecipeIngredients.recipe_id).order_by(
            Recipe.likes.desc())

class RecipeIngredients(db.Model):
    __tablename__ = 'recipeingredients'
    id = db.Column(db.Integer, primary_key = True)
    quantity = db.Column(db.Numeric)
    units = db.Column(db.String(140))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    usedingredients = db.relationship('Ingredients', secondary='link')
    def addingredients(self, ingredients):
        if not self.is_using(ingredients):
            self.usedingredients.append(ingredients)
    def removeingredients(self, ingredients):
        if self.is_using(ingredients):
            self.usedingredients.remove(ingredients)
    def is_using(self, ingredients):
        return self.usedingredients.filter(link.c.ingredients_id == ingredients.id).count() > 0

class Ingredients(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key = True)
    knownIngredients = db.Column(db.String(140))
    recipeingredient = db.relationship('RecipeIngredients', secondary='link')

class Link(db.Model):
    __tablename__ = 'link'
    recipeingredients_id = db.Column(db.Integer, db.ForeignKey('recipeingredients.id'), primary_key = True)
    ingredients_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key = True)
