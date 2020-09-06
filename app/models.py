from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    brand = db.Column(db.String(255), index=True)
    price = db.Column(db.Float(precision=2))
    in_stock_quantity = db.Column(db.Integer())

    def __repr__(self):
        return f"<Product {self.name}>"
