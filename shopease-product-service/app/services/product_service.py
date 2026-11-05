from datetime import datetime
from app.models.product_model import Product

# Temporary in-memory product storage
products_db = {}

# Auto-increment product ID
next_product_id = 1


# Create Product
def create_product(product_data: dict):
    global next_product_id

    product = Product(
        id=next_product_id,
        **product_data,
        created_at=datetime.now()
    )

    products_db[next_product_id] = product
    next_product_id += 1

    return product


# Get All Products
def get_all_products(
    category: str | None = None,
    skip: int = 0,
    limit: int = 10
):
    products = list(products_db.values())

    if category:
        products = [
            product for product in products
            if product.category.lower() == category.lower()
        ]

    return products[skip:skip + limit]


# Get Product By ID
def get_product_by_id(product_id: int):
    return products_db.get(product_id)


# Update Product
def update_product(product_id: int, update_data: dict):
    product = products_db.get(product_id)

    if product is None:
        return None

    for key, value in update_data.items():
        setattr(product, key, value)

    return product


# Delete Product
def delete_product(product_id: int):
    product = products_db.get(product_id)

    if product is None:
        return None

    del products_db[product_id]

    return product
