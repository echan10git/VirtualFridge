from flask import Flask, render_template, url_for, request
from forms import LoginForm, RegistrationForm
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import routes, models
from flask_login import LoginManager, logout_user, login_required
from werkzeug.urls import url_parse

app = Flask(__name__)
app.config['SECRET_KEY'] = '2a029ad143be63daaa6fd66e'
app.config.from_object(Config)
accountdb = SQLAlchemy(account)
migrateaccount = Migrate(account, accountdb)
login = LoginManager(app)
login.login_view = 'login'


@app.route("/")
def landing_page():
    return render_template('landing_page.html', title='Landing Page')

@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/myfridge")
@login_required
def myfridge():
    return render_template('myfridge.html', title='My Fridge')

@app.route("/search")
def search():
    return render_template('search.html', title='Search')

@app.route("/submit")
@login_required
def submit():
    return render_template('submit.html', title='Submit')

@app.route("/popular")
def popular():
    return render_template('popular.html', title='Popular')

@app.route("/help")
def help():
    return render_template('help.html', title='Help')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated: 
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flask('Congratulations, you are now registered!')
    return render_template('registration.html', title='Registration', form=form)