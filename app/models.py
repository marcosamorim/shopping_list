from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    brand = db.Column(db.String(255), index=True)
    price = db.Column(db.Float(precision=2))
    in_stock_quantity = db.Column(db.Integer())

    def __repr__(self):
        return f"<Product {self.name} - {self.brand}>"


@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    gift_list_id = db.relationship("GiftList", backref="gift_list", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


gifts = db.Table(
    "gifts",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),
    db.Column(
        "gift_list_id", db.Integer, db.ForeignKey("gift_list.id"), primary_key=True
    ),
    db.Column("gift_purchased", db.Boolean, default=False),
)


class GiftList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    products = db.relationship(
        "Product",
        secondary=gifts,
        lazy="subquery",
        backref=db.backref("gift_list", lazy=True),
    )

    def __repr__(self):
        return f"<GiftList {self.user_id}"
