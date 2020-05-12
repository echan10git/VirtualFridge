from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

@app.route("/")
def landing_page():
    return render_template('landing_page.html', title='Landing Page')

@app.route("/home")
@login_required
def home():
    return render_template('home.html', title='Home')

@app.route("/myfridge")
def myfridge():
    return render_template('myfridge.html', title='My Fridge')

@app.route("/search")
def search():
    return render_template('search.html', title='Search')

@app.route("/submit")
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
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route("/registration", methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration complete!')
        return redirect(url_for('login'))
    return render_template('registration.html', title="Registration", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/user/<username>') 
@login_required 
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)