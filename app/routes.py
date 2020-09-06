from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
import json


@app.route("/")
@app.route("/index")
def index():
    title = "Wedding Shop"
    return render_template("index.html", title=title)


@app.route("/list")
def product_list():
    title = "Product List"
    with open("products.json") as f:
        prod = f.read()

    products = json.loads(prod)
    return render_template("list.html", title=title, products=products)
# TODO: store the added products using ajax maybe?


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login requested for user {form.username.data}")
        return redirect("/index")
    return render_template("login.html", title="Sign In", form=form)


@app.route("/gift")
def gift_list():
    pass
