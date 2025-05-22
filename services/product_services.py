import sqlite3
from models.product import Product  
from models.category import Category 

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
    
    @staticmethod
    def get_all_categories():
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id_category, name, description FROM category
                """)
                rows = cursor.fetchall()
                return [Category(name=row[1], description=row[2], id_category=row[0]) for row in rows]
        except sqlite3.Error as e:
            print("Erreur SQLite :", e)
            return []
        
    @staticmethod
    def get_top_products(limit=3):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        p.id_product, p.name, p.description, p.price, p.stock_qty, p.id_category,
                        SUM(CAST(ci.qty AS INTEGER)) as total_sold
                    FROM product p
                    JOIN cart_item ci ON p.id_product = ci.id_product
                    GROUP BY p.id_product
                    ORDER BY total_sold DESC
                    LIMIT ?
                """, (limit,))
                rows = cursor.fetchall()
                return [
                    Product(
                        name=row[1],
                        description=row[2],
                        price=row[3],
                        stock_qty=row[4],
                        id_category=row[5],
                        id_product=row[0]
                    )
                    for row in rows
                ]
        except sqlite3.Error as e:
            print("Erreur SQLite :", e)
            return []

