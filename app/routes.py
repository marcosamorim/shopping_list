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
from app.models import Product, User, GiftList


# TODO: Improve index page
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
        user = User.query.filter_by(username=form.username.data).first_or_404(
            description=f'User "{form.username.data}" not found.'
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user)

        app.logger.info(f"User {user.username} logged in.")

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
        app.logger.info(f"User {user.username} registered.")
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
    user_gift_list_ids = current_user.product_ids()
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
    prod = Product.query.filter_by(id=prod_id).first_or_404(
        description=f"Product with id {prod_id} not found."
    )
    add_prod = GiftList(user_id=current_user.id, product_id=prod_id)
    db.session.add(add_prod)
    prod.in_stock_quantity -= 1
    db.session.commit()
    app.logger.info(f"Product id {prod_id} added to '{current_user.username}' gift list.")
    return redirect(url_for("product_list"))


@app.route("/remove_product", methods=["GET", "POST"])
@login_required
def remove_product_to_user_gift_list():
    # we only need the first (and only) key value from this form
    prod_id = request.form.keys().__next__()
    prod = Product.query.filter_by(id=prod_id).first_or_404(
        description=f"Product with id {prod_id} not found."
    )
    remove_prod = GiftList.query.filter_by(
        user_id=current_user.id, product_id=prod_id
    ).first()
    db.session.delete(remove_prod)
    prod.in_stock_quantity += 1
    db.session.commit()
    app.logger.info(f"Product id {prod_id} removed from '{current_user.username}' gift list.")
    return redirect(url_for("product_list"))


@app.route("/gift")
@login_required
def user_gift_list():
    products = current_user.products()
    purchased_user_products = [
        p.product_id
        for p in GiftList.query.filter_by(user_id=current_user.id, purchased=True).all()
    ]

    return render_template(
        "gift_list.html", username=current_user.username, products=products, purchased=purchased_user_products
    )


@app.route("/purchase_product", methods=["POST"])
@login_required
def purchase_product():
    prod_id = request.form.keys().__next__()
    purchase = GiftList.query.filter_by(
        user_id=current_user.id, product_id=prod_id
    ).first_or_404(f"Product {prod_id} for {current_user.username} not found.")
    purchase.purchased = True
    db.session.commit()
    app.logger.info(f"Product id {prod_id} purchased on '{current_user.username}' gift list.")

    return redirect(url_for("user_gift_list"))


# Gift List report
# -----------------------------
@app.route("/report")
@login_required
def gift_report():
    user_products = current_user.products()
    purchase_products_ids = [
        p.product_id
        for p in GiftList.query.filter_by(user_id=current_user.id, purchased=True).all()
    ]
    purchased_products = [p for p in user_products if p.id in purchase_products_ids]
    not_purchased_products = [p for p in user_products if p.id not in purchase_products_ids]

    return render_template(
        "report.html",
        username=current_user.username,
        user_products=user_products,
        purchased_products=purchased_products,
        not_purchased_products=not_purchased_products,
    )


# Error handling
# -----------------------------
@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f"Error 404: {error}")
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Error 500: {error}")
    db.session.rollback()
    return render_template("500.html"), 500
