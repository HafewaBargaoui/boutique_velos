import sqlite3
from datetime import datetime
import streamlit as st

DB_PATH = "databases/ecommerce.db"

class Cart:
    def __init__(self):
        if "cart" not in st.session_state:
            st.session_state.cart = {}

    def get_items(self):
        items = []
        for pid, item in st.session_state.cart.items():
            subtotal = round(item["price"] * item["qty"], 2)
            items.append({
                "id_product": pid,
                "name": item["name"],
                "price": item["price"],
                "qty": item["qty"],
                "subtotal": subtotal
            })
        return items

    def get_total(self):
        total = 0
        for item in st.session_state.cart.values():
            total += item["price"] * item["qty"]
        return round(total, 2)

    def remove_product(self, product_id):
        if product_id in st.session_state.cart:
            del st.session_state.cart[product_id]

    def clear_cart(self):
        st.session_state.cart = {}

    def checkout(self):
        """
        Enregistre la commande dans la base de données.
        Retourne (success: bool, message: str)
        """
        if not st.session_state.cart:
            return False, "Le panier est vide."

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Création du panier
            cursor.execute("INSERT INTO cart (total) VALUES (?)", (0,))
            cart_id = cursor.lastrowid

            # Création de la commande
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status = "pending"
            shipping_address = "10 rue de test, Paris"
            total_amount = 0
            cursor.execute(
                "INSERT INTO order_ (order_date, status, total_amount, shipping_adress) VALUES (?, ?, ?, ?)",
                (order_date, status, total_amount, shipping_address)
            )
            order_id = cursor.lastrowid

            total = 0
            for pid_str, item in st.session_state.cart.items():
                pid = int(pid_str)
                qty = item["qty"]

                cursor.execute("SELECT price, stock_qty FROM product WHERE Id_product = ?", (pid,))
                result = cursor.fetchone()
                if not result:
                    conn.rollback()
                    return False, f"Produit avec ID {pid} non trouvé."

                price, stock_qty = result

                if qty > stock_qty:
                    conn.rollback()
                    return False, f"Stock insuffisant pour le produit ID {pid}. Stock restant : {stock_qty}, demandé : {qty}"

                subtotal = price * qty
                total += subtotal

                # Insertion dans cart_item
                cursor.execute("""
                    INSERT INTO cart_item (Id_cart, Id_order, Id_product, subtotal, qty)
                    VALUES (?, ?, ?, ?, ?)
                """, (cart_id, order_id, pid, str(subtotal), str(qty)))

                # Mise à jour du stock produit
                new_stock = stock_qty - qty
                cursor.execute("""
                    UPDATE product SET stock_qty = ? WHERE Id_product = ?
                """, (new_stock, pid))

            # Mise à jour des totaux dans cart et order_
            cursor.execute("UPDATE cart SET total = ? WHERE Id_cart = ?", (total, cart_id))
            cursor.execute("UPDATE order_ SET total_amount = ? WHERE Id_order = ?", (total, order_id))

            # Informations utilisateur (fictif ici)
            user_id = 98
            cursor.execute("INSERT OR IGNORE INTO user_ (Id_user, username, email, password, user_type, vip) VALUES (?, ?, ?, ?, ?, ?)",
                        (user_id, 'john doe', 'john@example.com', 'hashed_password', 'customer', False))

            cursor.execute("SELECT 1 FROM customer WHERE Id_user = ?", (user_id,))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO customer (Id_user, address, Id_order, Id_cart) VALUES (?, ?, ?, ?)",
                            (user_id, shipping_address, order_id, cart_id))
            else:
                cursor.execute("UPDATE customer SET address = ?, Id_order = ?, Id_cart = ? WHERE Id_user = ?",
                            (shipping_address, order_id, cart_id, user_id))

            conn.commit()
            conn.close()

            self.clear_cart()
            st.session_state.checkout_ready = False

            return True, "Commande enregistrée avec succès !"

        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            return False, f"Erreur lors de la commande : {e}"
