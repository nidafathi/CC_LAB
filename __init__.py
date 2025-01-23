import json
from products import Product
from cart import dao
import products


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> "Cart":
        """
        Load a Cart object from a dictionary.
        """
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[Product(**content) for content in data['contents']],
            cost=data['cost']
        )


def get_cart(username: str) -> list[Product]:
    """
    Fetch cart details for a given username and return a list of Product objects.
    """
    # Fetch cart details from the DAO
    cart_details = dao.get_cart(username)

    # If no cart details exist, return an empty list
    if cart_details is None:
        return []

    # Safely parse the contents and fetch product details
    items = [
        content
        for cart_detail in cart_details
        for content in json.loads(cart_detail['contents'])
    ]

    # Fetch products directly using a map function
    return list(map(products.get_product, items))


def add_to_cart(username: str, product_id: int):
    """
    Add a product to the cart for a given username.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    """
    Remove a product from the cart for a given username.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    """
    Delete the entire cart for a given username.
    """
    dao.delete_cart(username)
