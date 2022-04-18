from flask import Blueprint, render_template, redirect, url_for , request , flash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods = ["GET" , "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("uname")
        password = request.form.get("psw")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('user does not exist.', category='error')

    return render_template("login.html")


@auth.route("/signup" , methods = ["GET" , "POST"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("user")
        psw1 = request.form.get("psw1")
        psw2 = request.form.get("psw2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif psw1 != psw2:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(psw1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                psw1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template("signup.html")


@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))