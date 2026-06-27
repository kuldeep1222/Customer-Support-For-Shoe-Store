## Tools.py

import json
import os


# Database File Paths

BASE_DIR = os.path.dirname("C:/Users/senku/Documents/gitcode/VScode for Python Projects/Customer_Support_Agent/Database")

PRODUCTS_FILE = os.path.join(BASE_DIR, "database", "products.json")
ORDERS_FILE = os.path.join(BASE_DIR, "database", "orders.json")


# Helper Functions

def load_products():
    """Load all products from products.json"""
    with open(PRODUCTS_FILE, "r") as file:
        return json.load(file)


def load_orders():
    """Load all orders from orders.json"""
    with open(ORDERS_FILE, "r") as file:
        return json.load(file)



# Tool 1 : Get Order

def get_order(order_id):
    """
    Return order details by order ID.
    """

    if not order_id:
        return None

    orders = load_orders()

    for order in orders:
        if order["order_id"].lower() == order_id.lower():
            return order

    return {
        "success": False,
        "error": "No order found with the given Order ID."
    }


# Tool 2 : Get Product

def get_product(product_id=None, name=None):
    """
    Return a product by ID or exact name.
    """

    products = load_products()

    if product_id:
        for product in products:
            if product["product_id"].lower() == product_id.lower():
                return product

    if name:
        for product in products:
            if product["name"].lower() == name.lower():
                return product

    return {
        "success": False,
        "error": "No product found with the given Product ID."
    }

# Tool 3 : Search Products

def search_products(
    brand=None,
    category=None,
    name=None,
    max_price=None,
    min_price=None,
    size=None,
    in_stock=None
):
    """
    Search products using optional filters.
    """

    products = load_products()
    results = []

    for product in products:

        if name:
            if name.lower() not in product["name"].lower():
                continue

        if brand:
            if brand.lower() != product["brand"].lower():
                continue

        if category:
            if category.lower() != product["category"].lower():
                continue

        if max_price is not None:
            if product["price"] > max_price:
                continue
        if min_price is not None:
            if product["price"] < min_price:
                continue
                
        if size is not None:
            if size not in product["sizes_available"]:
                continue

        if in_stock is not None:
            if product["in_stock"] != in_stock:
                continue

        results.append(product)

    return results


# Tool 4 : Compare Products

def compare_products(
    product1_id=None,
    product2_id=None,
    product1_name=None,
    product2_name=None
):
    """
    Compare two products by ID or name.
    Returns a structured comparison.
    """

    # Get first product
    if product1_id:
        product1 = get_product(product_id=product1_id)
    elif product1_name:
        product1 = get_product(name=product1_name)
    else:
        return None

    # Get second product
    if product2_id:
        product2 = get_product(product_id=product2_id)
    elif product2_name:
        product2 = get_product(name=product2_name)
    else:
        return None

    if not product1 or not product2:
        return None

    comparison = {
        "product_1": {
            "id": product1["product_id"],
            "name": product1["name"],
            "brand": product1["brand"],
            "category": product1["category"],
            "price": product1["price"],
            "sizes_available": product1["sizes_available"],
            "pieces_available": product1["pieces_available"],
            "in_stock": product1["in_stock"]
        },
        "product_2": {
            "id": product2["product_id"],
            "name": product2["name"],
            "brand": product2["brand"],
            "category": product2["category"],
            "price": product2["price"],
            "sizes_available": product2["sizes_available"],
            "pieces_available": product2["pieces_available"],
            "in_stock": product2["in_stock"]
        },
        "cheaper_product": (
            product1["product_id"]
            if product1["price"] < product2["price"]
            else product2["product_id"]
        ),
        "price_difference": abs(product1["price"] - product2["price"])
    }

    return comparison
    
# tool 5: find_alternatives
def find_alternatives(product_id=None, product_name=None, size=None):
    """
    Find cheaper alternatives for a product.

    Filters:
    - Same category
    - In stock
    - Cheaper than current product
    - Same size (if provided)
    """

    # Find target product
    if product_id:
        target_product = get_product(product_id=product_id)
    elif product_name:
        target_product = get_product(name=product_name)
    else:
        return None

    if not target_product:
        return None

    products = load_products()
    alternatives = []

    for product in products:

        # Skip the same product
        if product["product_id"] == target_product["product_id"]:
            continue

        # Same category
        if product["category"].lower() != target_product["category"].lower():
            continue

        # Must be in stock
        if not product["in_stock"]:
            continue

        # Must be cheaper
        if product["price"] >= target_product["price"]:
            continue

        # Size filter (optional)
        if size is not None:
            if size not in product["sizes_available"]:
                continue

        alternatives.append({
            "product_id": product["product_id"],
            "name": product["name"],
            "brand": product["brand"],
            "price": product["price"],
            "sizes_available": product["sizes_available"],
            "price_difference": target_product["price"] - product["price"]
        })

    # Cheapest first
    alternatives.sort(key=lambda x: x["price"])

    return alternatives


# Tool 6 : Recommend Products

def recommend_products(category, brand=None, max_price=None):
    """
    Recommend products based on category.

    Optional filters:
    - brand
    - max_price

    Only products that are in stock are returned.
    """

    if not category:
        return []

    products = load_products()
    recommendations = []

    for product in products:

        # Category filter
        if product["category"].lower() != category.lower():
            continue

        # Brand filter
        if brand and product["brand"].lower() != brand.lower():
            continue

        # Price filter
        if max_price is not None and product["price"] > max_price:
            continue

        # Stock filter
        if not product["in_stock"]:
            continue

        recommendations.append(product)

    # Sort by price (lowest first)
    recommendations.sort(key=lambda x: x["price"])

    return recommendations