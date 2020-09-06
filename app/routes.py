# from flask import render_template, flash, redirect
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    make_response,
)
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm
from app.models import Product, User


@app.route("/")
@app.route("/index")
def index():
    title = "Wedding Shop"
    return render_template("index.html", title=title)


# Login routes
# ---------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        # validate user login attempt
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)

        # if no next argument is specified, redirect to index
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Product related routes
# ------------------------------------
@login_required
@app.route("/list")
def product_list():
    title = "Product List"
    cookied_list = request.cookies.get("products")
    if cookied_list:
        products_on_list = Product.query.filter(id__in=cookied_list.split(","))
    else:
        products_on_list = []

    products = Product.query.all()
    return render_template(
        "list.html", title=title, products=products, products_on_list=products_on_list
    )


@login_required
@app.route("/gift")
def gift_list():
    pass
