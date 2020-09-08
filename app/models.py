from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    brand = db.Column(db.String(255), index=True)
    price = db.Column(db.Float(precision=2))
    in_stock_quantity = db.Column(db.Integer())

    def __repr__(self):
        return f"<Product {self.name} - {self.brand}>"


giftlist_products = db.Table(
    "gift_lists_products",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"),),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"),),
    db.Column("purchased", db.Boolean, default=False),
)


@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    products = db.relationship(
        "Product",
        secondary=giftlist_products,
        backref=db.backref("gifts", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
