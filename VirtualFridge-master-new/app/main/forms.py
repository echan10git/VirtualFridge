from flask import request
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _1
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
# from app import mall

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators = [Length(min=0, max = 140)])
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
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    steps = TextAreaField('Steps', validators = [Length(min=0, max = 140)])
    add = SubmitField('')
    submit = SubmitField('Done!')

class AddIngredientsForm(FlaskForm):
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    submit = SubmitField('Add')


