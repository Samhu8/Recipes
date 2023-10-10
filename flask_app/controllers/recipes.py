from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models import user

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/create', methods = ['POST'])
def new_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/create')
    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "date" : request.form["date"],
        "under" : request.form["under"],
        "user_id" : session["user_id"]
    }
    Recipe.save(data)
    return redirect('/login')

@app.route('/edit/<int:id>')
def edit_recipe(id):
    show_recipe = Recipe.show_one(id)
    return render_template('edit.html', recipe = show_recipe)

@app.route('/edit/<int:id>', methods=['POST'])
def update_recipe(id):
    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "date" : request.form["date"],
        "under" : request.form["under"],
        "id" : id
    }
    Recipe.edit_recipe(data)
    return redirect('/login')

@app.route('/show_one/<int:id>')
def show_one(id):
    view_recipe = Recipe.show_one(id)
    return render_template('show_one.html', view_recipe = view_recipe)

@app.route('/delete/<int:id>')
def delete_recipe(id):
    Recipe.delete_recipe(id)
    return redirect('/login')