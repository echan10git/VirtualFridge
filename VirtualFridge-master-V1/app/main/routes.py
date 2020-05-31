from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import db
from app.main.forms import EditProfileForm, EmptyForm, SearchForm, RecipeForm, AddIngredientsForm
from app.models import User, Fridges, Recipes, RecipeIngredients, Ingredients, Link, Linktwo
from app.main import bp

@bp.before_app_request
def before_request():
    db.session.commit()
    g.search_form = SearchForm()

@bp.route("/")
def landing_page():
    return render_template('landing_page.html', title='Landing Page')

@bp.route("/home")
@login_required
def home():
    return render_template('home.html', title='Home')

@bp.route("/recipesearch")
def recipe_search():
    return render_template('recipesearch.html', title='Recipe Search')

@bp.route("/myfridge")
def myfridge():
    return render_template('myfridge.html', title='My Fridge')

@bp.route("/submit", methods=['GET', 'POST'])
@login_required
def submit():
    form = RecipeForm()
    if form.validate_on_submit():
            recipe = Recipe(title = form.title.data, body = form.step.data, diet = form.hasDiet.data, spiceLevel = form.spiceLevel.data, user_id = current_user.id)
            db.session.add(recipe)
            db.session.commit()
    return render_template('recipe.html', title='Add a Recipe', form=form)

@bp.route("/popular")
def popular():
    return render_template('popular.html', title='Popular')

@bp.route("/help")
def help():
    return render_template('help.html', title='Help')

@bp.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Changes successfully made!')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@bp.route('/addingredientstest', methods=['GET', 'POST'])
def addingredientstest():
    form = AddIngredientsForm()
    if form.validate_on_submit():
        addition = Ingredients(form.ingredient.data)
        db.session.add(addition)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('addingredientstest.html', title = 'Add Ingredients', form=form)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@bp.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type = int)
    recipe, total = Recipes.search(g.search_form.q.data, page, current_app.config['RECIPES_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['RECIPES_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', recipe=recipe,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/addingredients')
def addingredients():
    if g.search_form.validate():
        if not current_app.elasticsearch:
            return redirect(url_for('main.home'))
        else:
            return redirect(url_for('addingredientstest.html'))
    if not g.search_form.validate():
        page = request.args.get('page', 1, type = int)
        ingredient, total = Ingredients.search(g.search_form.q.data, page, current_app.config['INGREDIENTS_PER_PAGE'])
        next_url = url_for('main.addingredients', q=g.search_form.q.data, page=page + 1) \
            if total > page * current_app.config['INGREDIENTS_PER_PAGE'] else None
        prev_url = url_for('main.addingredients', q=g.search_form.q.data, page=page - 1) \
            if page > 1 else None
        return render_template('addingredients.html', title='Add Ingredients', ingredient=ingredient,
                            next_url=next_url, prev_url=prev_url)
