from flask import Flask, render_template, url_for
from forms import LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '2a029ad143be63daaa6fd66e'


@app.route("/")
def landing_page():
    return render_template('landing_page.html', title='Landing Page')

@app.route("/home")
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
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    return render_template('registration.html', title='Registration', form=form)