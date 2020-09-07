from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
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
        login_user(user)

        # if no next argument is specified, redirect to index
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


# Product related routes
# ------------------------------------
@app.route("/list")
@login_required
def product_list():
    title = "Product List"
    # check if the user already have any product selected
    user_gift_list_ids = [p.id for p in current_user.products]
    if user_gift_list_ids:
        products_on_list = [
            p.id for p in Product.query.filter(Product.id.in_(user_gift_list_ids)).all()
        ]
    else:
        products_on_list = []

    products = Product.query.all()
    return render_template(
        "list.html", title=title, products=products, products_on_list=products_on_list
    )


@app.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product_to_user_gift_list():
    # we only need the first (and only) key value from this form
    prod_id = request.form.keys().__next__()
    prod = Product.query.filter_by(id=prod_id).first()
    current_user.products.append(prod)
    prod.in_stock_quantity -= 1
    db.session.commit()
    return redirect(url_for("product_list"))


@app.route("/remove_product", methods=["GET", "POST"])
@login_required
def remove_product_to_user_gift_list():
    # we only need the first (and only) key value from this form
    prod_id = request.form.keys().__next__()
    prod = Product.query.filter_by(id=prod_id).first()
    print("current_user.products")
    print(current_user.products)
    current_user.products.remove(prod)
    prod.in_stock_quantity += 1
    db.session.commit()
    return redirect(url_for("product_list"))


# TODO: show user's gift list
@app.route("/gift")
@login_required
def gift_list():
    pass


# Error handling
# -----------------------------
@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500
