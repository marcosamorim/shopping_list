"""seed products

Revision ID: 3132bb8ec2ea
Revises: da8d0909826c
Create Date: 2020-09-09 21:47:59.529720

"""
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Float
from alembic import op


# revision identifiers, used by Alembic.
revision = '3132bb8ec2ea'
down_revision = 'da8d0909826c'
branch_labels = None
depends_on = None


# Create an ad-hoc table to use for the insert statement.
products_table = table(
    "products",
    column("id", Integer),
    column("name", String),
    column("brand", String),
    column("price", Float),
    column("in_stock_quantity", Integer),
)

seed_data = [
    {
        "id": 1,
        "name": "Tea pot",
        "brand": "Le Creuset",
        "price": "47.00GBP",
        "in_stock_quantity": 50,
    },
    {
        "id": 2,
        "name": "Cast Iron Oval Casserole - 25cm; Volcanic",
        "brand": "Le Creuset",
        "price": "210.00GBP",
        "in_stock_quantity": 27,
    },
    {
        "id": 4,
        "name": "Gordon Ramsay Maze 12 Piece Set, White",
        "brand": "ROYAL DOULTON",
        "price": "85.00GBP",
        "in_stock_quantity": 2,
    },
    {
        "id": 5,
        "name": "9-speed Hand Mixer; Almond Cream",
        "brand": "KITCHENAID",
        "price": "99.99GBP",
        "in_stock_quantity": 9,
    },
    {
        "id": 6,
        "name": "Mini Stand Mixer; Empire Red",
        "brand": "KITCHENAID",
        "price": "399.00GBP",
        "in_stock_quantity": 2,
    },
    {
        "id": 7,
        "name": "50's Style Stand Mixer, Full-Colour White",
        "brand": "SMEG SMALL APPLIANCES",
        "price": "449.00GBP",
        "in_stock_quantity": 0,
    },
    {
        "id": 8,
        "name": "50's Style Stand Mixer, Black",
        "brand": "SMEG SMALL APPLIANCES",
        "price": "449.99GBP",
        "in_stock_quantity": 1,
    },
    {
        "id": 9,
        "name": "Polka Bedding Set, King, Silver",
        "brand": "BEAU LIVING",
        "price": "105.00GBP",
        "in_stock_quantity": 5,
    },
    {
        "id": 10,
        "name": "Paignton Bedding Set, King, White",
        "brand": "BEAU LIVING",
        "price": "105.00GBP",
        "in_stock_quantity": 0,
    },
    {
        "id": 11,
        "name": "Original Kettle E-5710 Charcoal Barbecue - 57cm; Black",
        "brand": "WEBER GRILLS",
        "price": "199.99GBP",
        "in_stock_quantity": 1,
    },
    {
        "id": 12,
        "name": "Compact Charcoal Grill, 57 cm",
        "brand": "WEBER GRILLS",
        "price": "139.99GBP",
        "in_stock_quantity": 29,
    },
    {
        "id": 13,
        "name": "Falcon T2 Square Parasol, 2.7m, Taupe",
        "brand": "GARDENSTORE",
        "price": "344.99GBP",
        "in_stock_quantity": 5,
    },
    {
        "id": 14,
        "name": "Riva Round Parasol - 3m; Anthracite",
        "brand": "GARDENSTORE",
        "price": "79.99GBP",
        "in_stock_quantity": 8,
    },
    {
        "id": 15,
        "name": "Glow Challenger T2 Square Parasol - 3m, Taupe",
        "brand": "GARDENSTORE",
        "price": "619.99GBP",
        "in_stock_quantity": 30,
    },
    {
        "id": 16,
        "name": "Ceramic Bottle Lamp, Small",
        "brand": "THE WHITE COMPANY",
        "price": "95.00GBP",
        "in_stock_quantity": 0,
    },
    {
        "id": 17,
        "name": "Gold Sitting Mouse Lamp",
        "brand": "GRAHAM & GREEN",
        "price": "73.00GBP",
        "in_stock_quantity": 3,
    },
    {
        "id": 18,
        "name": "Usha Mango Wood Lamp Base",
        "brand": "NKUKU",
        "price": "49.95GBP",
        "in_stock_quantity": 12,
    },
    {
        "id": 19,
        "name": "Sea Green Honeycomb Glass Lamp",
        "brand": "GRAHAM & GREEN",
        "price": "95.00GBP",
        "in_stock_quantity": 4,
    },
    {
        "id": 20,
        "name": "Faux Tortoiseshell Lamp",
        "brand": "OKA",
        "price": "175.00GBP",
        "in_stock_quantity": 0,
    },
    {
        "id": 21,
        "name": "2 Person Blue Tweed Hamper",
        "brand": "WILLOW STORE",
        "price": "85.50GBP",
        "in_stock_quantity": 2,
    },
]

# Convert price on seed_data to float
for prod in seed_data:
    try:
        float_price = prod["price"].strip("GBP")
        prod["price"] = float(float_price)
    except (KeyError, SyntaxError, AttributeError):
        prod["price"] = 0.0


def upgrade():
    op.bulk_insert(products_table, seed_data)


def downgrade():
    op.drop_table("products")
