import sqlite3
from datetime import datetime

DB_PATH = "databases/ecommerce.db"

class Cart:
    """
    Classe représentant un panier d'achat.
    Gère les opérations de création, ajout, suppression de produits, et calcul du total.
    """

    def __init__(self, cart_id=None):
        """
        Initialise une instance de panier.
        Si aucun ID de panier n'est fourni, un nouveau panier est créé automatiquement.

        Args:
            cart_id (int, optional): ID d'un panier existant. Defaults to None.
        """
        self.cart_id = cart_id
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        if self.cart_id is None:
            self.create_cart()

    def create_cart(self):
        """
        Crée un nouveau panier dans la base de données avec un total initial de 0.
        L'attribut `cart_id` est mis à jour avec l'ID nouvellement créé.
        """
        self.cursor.execute("INSERT INTO cart (total) VALUES (0)")
        self.cart_id = self.cursor.lastrowid
        self.conn.commit()

    def add_product(self, product_id, qty):
        """
        Ajoute un produit au panier ou le met à jour s'il existe déjà.

        Args:
            product_id (int): ID du produit à ajouter.
            qty (int): Quantité du produit.

        Raises:
            ValueError: Si le produit n'existe pas dans la base de données.
        """
        self.cursor.execute("SELECT price FROM product WHERE Id_product = ?", (product_id,))
        product = self.cursor.fetchone()
        if not product:
            raise ValueError("Produit introuvable")

        price = product["price"]
        subtotal = round(price * qty, 2)

        self.cursor.execute("""
            INSERT OR REPLACE INTO cart_item (Id_cart, Id_order, Id_product, subtotal, qty)
            VALUES (?, NULL, ?, ?, ?)
        """, (self.cart_id, product_id, str(subtotal), str(qty)))

        self.update_total()
        self.conn.commit()

    def remove_product(self, product_id):
        """
        Supprime un produit du panier.

        Args:
            product_id (int): ID du produit à retirer.
        """
        self.cursor.execute("""
            DELETE FROM cart_item
            WHERE Id_cart = ? AND Id_product = ?
        """, (self.cart_id, product_id))
        self.update_total()
        self.conn.commit()

    def get_items(self):
        """
        Récupère les articles du panier avec leurs détails.

        Returns:
            list[sqlite3.Row]: Liste des produits dans le panier (nom, prix, quantité, sous-total).
        """
        self.cursor.execute("""
            SELECT p.name, p.price, ci.qty, ci.subtotal
            FROM cart_item ci
            JOIN product p ON p.Id_product = ci.Id_product
            WHERE ci.Id_cart = ?
        """, (self.cart_id,))
        return self.cursor.fetchall()

    def update_total(self):
        """
        Recalcule le total du panier à partir des sous-totaux des articles.
        Met à jour le champ `total` de la table `cart`.
        """
        self.cursor.execute("""
            SELECT SUM(CAST(subtotal AS REAL)) as total
            FROM cart_item
            WHERE Id_cart = ?
        """, (self.cart_id,))
        result = self.cursor.fetchone()
        total = result["total"] if result["total"] is not None else 0
        self.cursor.execute("UPDATE cart SET total = ? WHERE Id_cart = ?", (total, self.cart_id))

    def delete_cart(self):
        """
        Supprime complètement le panier et tous ses articles de la base de données.
        Réinitialise l'attribut `cart_id`.
        """
        self.cursor.execute("DELETE FROM cart_item WHERE Id_cart = ?", (self.cart_id,))
        self.cursor.execute("DELETE FROM cart WHERE Id_cart = ?", (self.cart_id,))
        self.conn.commit()
        self.cart_id = None

    def get_total(self):
        """
        Récupère le total actuel du panier.

        Returns:
            float: Montant total du panier.
        """
        self.cursor.execute("SELECT total FROM cart WHERE Id_cart = ?", (self.cart_id,))
        result = self.cursor.fetchone()
        return result["total"] if result else 0

    def __del__(self):
        """
        Ferme la connexion à la base de données à la destruction de l'objet.
        """
        self.conn.close()
