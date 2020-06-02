from flask import request
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _1
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, Ingredients
# from app import mall

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators = [Length(min=0, max = 140)])
    diet = StringField('Diet', validators = [Length(min=0, max = 140)])
    submit = SubmitField('Submit')
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    step = TextAreaField('Step',validators=[DataRequired()])
    hasDiet = StringField('Is there a special diet associated with this recipe? (If none, write N/A)', validators=[DataRequired()])
    spiceLevel = IntegerField('How spicy is your recipe on a scale of 1 to 5?', validators=[DataRequired()])
    submit = SubmitField('Add Ingredients!')

class AddIngredientsForm(FlaskForm):
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_ingredient(self, knownIngredients):
        ingredients = Ingredients.query.filter_by(knownIngredients=knownIngredients.data).first()
        if ingredients is not None:
            raise ValidationError('Already added!')


