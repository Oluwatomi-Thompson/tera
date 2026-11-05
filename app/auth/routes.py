from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from urllib.parse import urlsplit

from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm
from app.extensions import db
from app.lessons.utils import calculate_progress
from app.models import User


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("An account with that email already exists. Try logging in instead.", "error")
            return render_template("auth/register.html", form=form)

        user = User(email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Welcome to Tera — let's start with the basics.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash("Incorrect email or password.", "error")
            return render_template("auth/login.html", form=form)

        login_user(user, remember=form.remember_me.data)
        flash("Welcome back.", "success")
        next_url = request.args.get("next")
        if not next_url or urlsplit(next_url).netloc != "":
            next_url = url_for("main.dashboard")
        return redirect(next_url)

    return render_template("auth/login.html", form=form)


@bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "info")
    return redirect(url_for("main.index"))


@bp.get("/profile")
@login_required
def profile():
    progress = calculate_progress(current_user)
    return render_template("auth/profile.html", progress=progress)
