from models.cart import Cart
import sqlite3
import os

# Détermine dynamiquement le chemin absolu vers la base de données
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "databases", "ecommerce.db")


def get_cart(cart_id=None):
    """
    Récupère une instance de panier existant ou crée un nouveau panier si aucun ID n'est fourni.

    Args:
        cart_id (int, optional): ID du panier existant. Defaults to None.

    Returns:
        Cart: Instance de la classe Cart.
    """
    conn = sqlite3.connect(DB_PATH)
    cart = Cart(conn, cart_id)
    return cart


def create_new_cart():
    """
    Crée un nouveau panier vide dans la base de données.

    Returns:
        int: ID du nouveau panier.
    """
    conn = sqlite3.connect(DB_PATH)
    cart = Cart(conn)
    new_cart_id = cart.create_cart()
    conn.close()
    return new_cart_id


def add_product_to_cart(cart_id, product_id, qty):
    """
    Ajoute un produit à un panier existant.

    Args:
        cart_id (int): ID du panier.
        product_id (int): ID du produit à ajouter.
        qty (int): Quantité du produit.
    """
    conn = sqlite3.connect(DB_PATH)
    cart = Cart(conn, cart_id)
    cart.add_item(product_id, qty)
    conn.close()


def remove_product_from_cart(cart_id, product_id):
    """
    Supprime un produit d'un panier.

    Args:
        cart_id (int): ID du panier.
        product_id (int): ID du produit à retirer.
    """
    conn = sqlite3.connect(DB_PATH)
    cart = Cart(conn, cart_id)
    cart.remove_item(product_id)
    conn.close()


def get_cart_items(cart_id):
    """
    Récupère la liste des produits contenus dans un panier.

    Args:
        cart_id (int): ID du panier.

    Returns:
        list[sqlite3.Row]: Liste des articles dans le panier.
    """
    conn = sqlite3.connect(DB_PATH)
    cart = Cart(conn, cart_id)
    items = cart.get_items()
    conn.close()
    return items


def get_cart_total(cart_id):
    """
    Récupère le montant total du panier.

    Args:
        cart_id (int): ID du panier.

    Returns:
        float: Total du panier.
    """
    conn = sqlite3.connect(DB_PATH)
    cart = Cart(conn, cart_id)
    total = cart.calculate_total()
    conn.close()
    return total
