import sqlite3

def add_cart_item(cart_id: int, product_id: int, qty: int, conn: sqlite3.Connection):
    """
    Ajoute un produit au panier dans la table cart_item.
    
    Si le produit est déjà présent pour ce panier, il est remplacé (INSERT OR REPLACE).
    Le sous-total est calculé automatiquement.

    Args:
        cart_id (int): ID du panier.
        product_id (int): ID du produit à ajouter.
        qty (int): Quantité du produit à ajouter.
        conn (sqlite3.Connection): Connexion active à la base de données.

    Raises:
        ValueError: Si le produit n'existe pas dans la base de données.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM product WHERE Id_product = ?", (product_id,))
    row = cursor.fetchone()
    
    if not row:
        raise ValueError("Produit introuvable")

    price = row[0]
    subtotal = round(price * qty, 2)

    cursor.execute("""
        INSERT OR REPLACE INTO cart_item (Id_cart, Id_order, Id_product, subtotal, qty)
        VALUES (?, NULL, ?, ?, ?)
    """, (cart_id, product_id, str(subtotal), str(qty)))

    conn.commit()

def remove_cart_item(cart_id: int, product_id: int, conn: sqlite3.Connection):
    """
    Supprime un produit du panier dans la table cart_item.

    Args:
        cart_id (int): ID du panier.
        product_id (int): ID du produit à supprimer.
        conn (sqlite3.Connection): Connexion active à la base de données.
    """
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM cart_item
        WHERE Id_cart = ? AND Id_product = ?
    """, (cart_id, product_id))
    conn.commit()

def get_cart_items(cart_id: int, conn: sqlite3.Connection):
    """
    Récupère tous les produits d’un panier donné avec leurs détails (nom, prix, quantité, sous-total).

    Args:
        cart_id (int): ID du panier.
        conn (sqlite3.Connection): Connexion active à la base de données.

    Returns:
        list[sqlite3.Row]: Liste des lignes contenant les informations sur chaque article du panier.
    """
    cursor = conn.cursor()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name, p.price, ci.qty, ci.subtotal
        FROM cart_item ci
        JOIN product p ON p.Id_product = ci.Id_product
        WHERE ci.Id_cart = ?
    """, (cart_id,))
    return cursor.fetchall()

def clear_cart(cart_id: int, conn: sqlite3.Connection):
    """
    Supprime tous les articles du panier (nettoie complètement le cart_id donné).

    Args:
        cart_id (int): ID du panier.
        conn (sqlite3.Connection): Connexion active à la base de données.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart_item WHERE Id_cart = ?", (cart_id,))
    conn.commit()
