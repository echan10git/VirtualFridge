from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, db
from hashlib import md5
from app.search import add_to_index, remove_from_index, query_index

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

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

    def get_reset_password_token(self, expires_in = 600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

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

class Recipes(SearchableMixin, db.Model):
    __searchable__ = ['title']
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    RecipeIngredient = db.relationship('RecipeIngredients', backref='recipeorigin', lazy = 'dynamic')
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

