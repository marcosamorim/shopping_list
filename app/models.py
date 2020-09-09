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


class GiftList(db.Model):
    __tablename__ = "giftlists"
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), primary_key=True, index=True
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), primary_key=True, index=True
    )
    purchased = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<GiftList {self.username()} - {self.product()}"

    def username(self):
        return User.query.filter_by(id=self.user_id).first().username

    def product(self):
        return Product.query.filter_by(id=self.product_id).first()


@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def products(self):
        user_prod_ids = [p.product_id for p in GiftList.query.filter_by(user_id=self.id).all()]
        products = Product.query.filter(Product.id.in_(user_prod_ids)).all()
        return products

    def product_ids(self):
        return [p.id for p in self.products()]
