import sqlite3
from models.product import Product  

DB_PATH = "databases/ecommerce.db"

class ProductService:

    @staticmethod
    def get_all_products():
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id_product, name, description, price, stock_qty, id_category FROM product
                """)
                rows = cursor.fetchall()
                return [Product(name=row[1], description=row[2], price=row[3], stock_qty=row[4],id_category=row[5], id_product=row[0]) for row in rows]
        except sqlite3.Error as e:
            print("Erreur SQLite :", e)
            return []

    @staticmethod
    def get_product_by_id(product_id: int):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id_product, name, description, price, stock_qty, image, id_category FROM product
                    WHERE id_product = ?
                """, (product_id,))
                row = cursor.fetchone()
                if row:
                    return Product(name=row[1], description=row[2], price=row[3], stock_qty=row[4], id_category=row[5], id_product=row[0])
                else:
                    print(f"Aucun produit trouvé avec l'ID {product_id}")
                    return None
        except sqlite3.Error as e:
            print("Erreur SQLite :", e)
            return None
        
# services/product_service.py
from models.product import Product

def get_top_products():
    return [
        Product(
            id_product=1,
            name="Vélo de Montagne",
            description="Un VTT robuste pour les sentiers difficiles.",
            price=599,
            stock_qty=10,
            id_category=1
        ),
        Product(
            id_product=2,
            name="Vélo de Route",
            description="Léger et rapide, parfait pour la compétition.",
            price=1299,
            stock_qty=7,
            id_category=1
        ),
        Product(
            id_product=3,
            name="Vélo Électrique",
            description="Assistance électrique pour les trajets quotidiens.",
            price=1690,
            stock_qty=5,            image="assets/offrorad_anywhere_bike.jpg",

            id_category=1
        ),
    ]
