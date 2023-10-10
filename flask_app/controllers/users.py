from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user
from flask_app.models import recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


#*********** MAIN PAGE

@app.route('/')
def main_page():
    return render_template('index.html')

#*********** CREATE USER

@app.route('/register', methods=["POST"])
def register():
    if not user.User.validate_login(request.form):
        return redirect('/')
    if not user.User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    if request.form['password'] != request.form['confirm_password']:
        flash("Password is not matching. Please try again.")
        return redirect('/')
    user_id = user.User.save(data)
    session['user_id'] = user_id
    return redirect("/")

#************* LOGIN USER

@app.route('/login', methods=["POST"])
def login():
    data = {"email" : request.form["email"],}
    user_in_db = user.User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/login")

@app.route('/login')
def logged_in():
    data = {
        "id" : session['user_id']
    }
    logged_in_user = user.User.get_by_id(data)
    return render_template('login_page.html', user = logged_in_user, recipe_info = recipe.Recipe.show_all_recipes())

#************************* LOGOUT

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')