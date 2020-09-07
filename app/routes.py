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
    cookied_list = request.cookies.get("products")
    if cookied_list:
        products_on_list = Product.query.filter(id__in=cookied_list.split(","))
    else:
        products_on_list = []

    products = Product.query.all()
    return render_template(
        "list.html", title=title, products=products, products_on_list=products_on_list
    )


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
