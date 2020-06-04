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

@bp.route("/help")
def help():
    return render_template('help.html', title='Help')

@bp.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.diet = form.diet.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Changes successfully made!')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.diet.data = current_user.diet
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
    currentingredient = []
    recipeids = []
    for fridges in current_user.fridge:
        for ingredients in fridges.currentingredients:
            currentingredient.append(ingredients.id)
    for recipes in recipe:
        r = []
        for recipeingredients in recipes.ingredientsinrecipe:
            for ingredients in recipeingredients.usedingredients:
                r.append(ingredients.id)
        check =  all(item in currentingredient for item in r)
        if check is True:
            recipeids.append(recipes.id)
    when = []
    for i in range(len(recipeids)):
        when.append((recipeids[i], i))
    recipe = Recipes.query.filter(Recipes.id.in_(recipeids))
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['RECIPES_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', recipe=recipe,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/addingredients')
def addyouringredients():
    if not g.search_form.validate():
            return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type = int)
    ingredient, total = Ingredients.search(g.search_form.q.data, page, current_app.config['INGREDIENTS_PER_PAGE'])
    next_url = url_for('main.addingredients', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['INGREDIENTS_PER_PAGE'] else None
    prev_url = url_for('main.addingredients', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('addingredients.html', title='Add Ingredients', ingredient=ingredient,
                        next_url=next_url, prev_url=prev_url)

@bp.route('/added/<int:ingredientsid>')
def add(ingredientsid):
    ingredient = Ingredients.query.get(ingredientsid)
    fridgenew = Fridges(quantity = 1)
    fridgenew.currentingredients.append(ingredient)
    current_user.fridge.append(fridgenew)
    db.session.commit()
    return redirect(url_for('main.myfridge'))

@bp.route("/submit", methods=['GET', 'POST'])
@login_required
def submit():
    form = RecipeForm()
    if form.validate_on_submit():
            recipe = Recipes(title = form.title.data, body = form.step.data, diet = form.hasDiet.data, spiceLevel = form.spiceLevel.data, popularity = 0, user_id = current_user.id)
            current_user.recipe.append(recipe)
            db.session.commit()
            return redirect(url_for('main.recipeingredientssearch', recipesid=recipe.id))
    return render_template('recipe.html', title='Add a Recipe', form=form)

@bp.route('/recipeingredientssearch/<int:recipesid>')
def recipeingredientssearch(recipesid):
    recipes = Recipes.query.get(recipesid)
    return render_template('recipeingredientssearch.html', title='Add Ingredients to Your Recipe', recipesid=recipesid, recipes = recipes)

@bp.route('/addingredientstorecipe/<int:recipesid>')
def addingredientstorecipe(recipesid):
    if not g.search_form.validate():
            return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type = int)
    ingredient, total = Ingredients.search(g.search_form.q.data, page, current_app.config['INGREDIENTS_PER_PAGE'])
    next_url = url_for('main.addingredientstorecipe', q=g.search_form.q.data, page=page + 1, recipesid = recipesid) \
        if total > page * current_app.config['INGREDIENTS_PER_PAGE'] else None
    prev_url = url_for('main.addingredientstorecipe', q=g.search_form.q.data, page=page - 1, recipesid = recipesid) \
        if page > 1 else None
    return render_template('addingredientstorecipe.html', title='Add Ingredients', ingredient=ingredient,
                        next_url=next_url, prev_url=prev_url, recipesid = recipesid)

@bp.route('/addquantityrecipes/<int:recipesid>/<int:recipeingredientsid>/<int:ingredientsid>')
def addquantityrecipe(recipesid, recipeingredientsid, ingredientsid):
    recipeingredient = RecipeIngredients.query.filter(RecipeIngredients.id == recipeingredientsid)
    recipeingredient.first().quantity = recipeingredient.first().quantity + 1
    db.session.commit()
    return redirect(url_for('main.recipeingredientssearch', recipesid=recipesid))

@bp.route('/removequantityrecipes//<int:recipesid>/<int:recipeingredientsid>/<int:ingredientsid>')
def removequantityrecipe(recipesid, recipeingredientsid, ingredientsid):
    recipeingredient = RecipeIngredients.query.filter(RecipeIngredients.id == recipeingredientsid)
    recipeingredient.first().quantity = recipeingredient.first().quantity - 1
    if recipeingredient.first().quantity <= 0:
        Link.query.filter_by(recipeingredients_id = recipeingredientsid).delete()
        RecipeIngredients.query.filter(RecipeIngredients.id == recipeingredientsid).delete()
    db.session.flush()
    db.session.commit()
    return redirect(url_for('main.recipeingredientssearch', recipesid=recipesid))

@bp.route('/addedtorecipe/<int:ingredientsid>/<int:recipesid>')
def addedtorecipe(ingredientsid, recipesid):
    ingredient = Ingredients.query.get(ingredientsid)
    recipes = Recipes.query.get(recipesid)
    ingredientnew = RecipeIngredients(quantity = 1, units = 'grams')
    ingredientnew.usedingredients.append(ingredient)
    recipes.ingredientsinrecipe.append(ingredientnew)
    db.session.commit()
    return redirect(url_for('main.recipeingredientssearch', recipesid = recipesid))

@bp.route('/removerecipe/<int:recipesid>')
def removerecipe(recipesid):
    recipes = Recipes.query.get(recipesid)
    for recipeingredients in recipes.ingredientsinrecipe:
        Link.query.filter_by(recipeingredients_id = recipeingredients.id).delete()
    Recipes.query.filter(Recipes.id == recipesid).delete()
    db.session.flush()
    db.session.commit()
    return redirect(url_for('main.user', username=current_user.username))

@bp.route('/recipe/<recipeid>')
@login_required
def recipe(recipeid):
    recipe = Recipes.query.filter(Recipes.id==recipeid).first_or_404()
    if current_user.id != recipe.author.id:
        recipe.popularity = recipe.popularity + 1
    return render_template('recipeview.html', recipe=recipe)

@bp.route('/addquantity/<int:fridgesid>')
def addquantity(fridgesid):
    fridge = Fridges.query.get(fridgesid)
    fridge.quantity = fridge.quantity + 1
    db.session.commit()
    return redirect(url_for('main.myfridge'))

@bp.route('/removequantity/<int:fridgesid>')
def removequantity(fridgesid):
    fridge = Fridges.query.get(fridgesid)
    fridge.quantity = fridge.quantity - 1
    if fridge.quantity <= 0:
        Linktwo.query.filter_by(fridges_id = fridgesid).delete()
        Fridges.query.filter(Fridges.id == fridgesid).delete()
    db.session.flush()
    db.session.commit()
    return redirect(url_for('main.myfridge'))
