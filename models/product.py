import sqlite3
DB_PATH = "databases/ecommerce.db"
class Product:
    def __init__(self, name, description, price, stock_qty, id_product=None):
        self.id_product = id_product
        self.name = name
        self.description = description
        self.price = price
        self.stock_qty = stock_qty
    def add_product(self):
        try:
            if self.id_product is not None:
                print("L'ajout est bloqué : l'ID du produit est déjà défini.")
                return

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO product (name, description, price, stock_qty)
                    VALUES (?, ?, ?, ?)
                """, (self.name, self.description, self.price, self.stock_qty))
                self.id_product = cursor.lastrowid
                conn.commit()
                print(f"Produit ajouté avec l'ID {self.id_product}")
        except sqlite3.Error as e:
            print("Erreur SQLite :", e)