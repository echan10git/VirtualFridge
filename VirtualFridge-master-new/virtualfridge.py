from app import create_app, db
from app.models import User, Fridges, Recipes, RecipeIngredients, Ingredients, Link

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
