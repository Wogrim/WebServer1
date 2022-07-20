from flask_app import app, bcrypt

from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.language import Language


@app.route("/")
def _login_register():
    if 'user_id' in session:
        return redirect("/main")
    #else
    languages = Language.read_all()
    return render_template("login_register.html",languages=languages)

@app.route("/main")
def _main():
    if 'user_id' not in session:
        return redirect("/")
    #else
    data = {'id':session['user_id']}
    user = User.read_one_by_id(data)
    return render_template("main.html",user=user)

@app.route("/logout")
def _logout():
    if 'user_id' in session:
        del session['user_id']
    return redirect("/")

@app.route("/register", methods=['POST'])
def _register():
    print(request.form)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password'],
        'birthdate': request.form['birthdate'],
        'language_id': request.form['language_id']
    }
    if not User.validate(data):
        return redirect("/")
    #else
    data['password'] = bcrypt.generate_password_hash(data['password'])
    id = User.create(data)
    session['user_id'] = id
    return redirect("/main")

login_fail_message = "email and/or password incorrect"

@app.route("/login", methods=['POST'])
def _login():
    data = {
        'email': request.form['email']
    }

    user = User.read_one_by_email(data)
    if not user:
        flash(login_fail_message,'login')
        return redirect("/")
    #else
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash(login_fail_message,'login')
        return redirect("/")
    #else

    session['user_id'] = user.id
    return redirect("/main")