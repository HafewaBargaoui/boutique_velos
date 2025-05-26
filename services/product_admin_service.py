import sqlite3
from models.product import Product
from models.category import Category
import pandas as pd

DB_PATH = "databases/ecommerce.db"

class ProductAdminService:

    @staticmethod
    def get_all_products():
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_product, name, description, price, stock_qty, id_category
                FROM product
            """)
            rows = cursor.fetchall()
            return [Product(id_product=row[0], name=row[1], description=row[2], price=row[3], stock_qty=row[4], id_category=row[5]) for row in rows]

    @staticmethod
    def add_product(name, description, price, stock_qty, id_category):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO product (name, description, price, stock_qty, id_category)
                VALUES (?, ?, ?, ?, ?)
            """, (name, description, price, stock_qty, id_category))
            conn.commit()

    @staticmethod
    def update_product(id_product, name, description, price, stock_qty, id_category):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE product
                SET name = ?, description = ?, price = ?, stock_qty = ?, id_category = ?
                WHERE id_product = ?
            """, (name, description, price, stock_qty, id_category, id_product))
            conn.commit()

    @staticmethod
    def delete_product(id_product):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM product WHERE id_product = ?
            """, (id_product,))
            conn.commit()

    @staticmethod
    def get_all_categories():
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_category, name, description FROM category
            """)
            rows = cursor.fetchall()
            return [Category(id_category=row[0], name=row[1], description=row[2]) for row in rows]

    @staticmethod
    def get_all_orders():
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query("""
                SELECT 
                    o.Id_order AS id_order,
                    o.order_date,
                    o.status,
                    o.total_amount,
                    o.shipping_adress,
                    u.username,
                    u.email
                FROM order_ o
                JOIN user_ u ON o.Id_user = u.Id_user
                ORDER BY o.order_date DESC
            """, conn)


    @staticmethod
    def get_order_details(order_id):
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query("""
                SELECT p.name, ci.qty, ci.subtotal
                FROM cart_item ci
                JOIN product p ON ci.id_product = p.id_product
                WHERE ci.id_order = ?
            """, conn, params=(order_id,))
