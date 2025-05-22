import sqlite3
from datetime import datetime

def test_create_cart():
    """ script pour tester si les codes s'accordent entre eux."""
    conn = sqlite3.connect("databases/ecommerce.db")
    cursor = conn.cursor()

    # Étape 1 : Créer un nouveau panier
    cursor.execute("INSERT INTO cart (total) VALUES (?)", (0,))
    cart_id = cursor.lastrowid
    print(f" Nouveau panier créé : Id_cart = {cart_id}")

    # Étape 2 : Créer une commande
    order_date = datetime.now().strftime("%Y-%m-%d")
    status = "pending"
    shipping_address = "10 rue de test, Paris"
    total_amount = 0  
    cursor.execute(
        "INSERT INTO order_ (order_date, status, total_amount, shipping_adress) VALUES (?, ?, ?, ?)",
        (order_date, status, total_amount, shipping_address)
    )
    order_id = cursor.lastrowid
    print(f" Nouvelle commande créée : Id_order = {order_id}")

    # Étape 3 : Ajouter des articles
    items_to_add = [
        {"product_id": 1, "qty": 1},
        {"product_id": 3, "qty": 2},
    ]

    total = 0
    for item in items_to_add:
        cursor.execute("SELECT price FROM product WHERE Id_product = ?", (item["product_id"],))
        price = cursor.fetchone()[0]
        subtotal = price * item["qty"]
        total += subtotal

        cursor.execute("""
            INSERT INTO cart_item (Id_cart, Id_order, Id_product, subtotal, qty)
            VALUES (?, ?, ?, ?, ?)
        """, (cart_id, order_id, item["product_id"], str(subtotal), str(item["qty"])))

    print(f" Articles ajoutés au panier. Total: {total:.2f} €")

    # Étape 4 : Mettre à jour le total du panier et de la commande
    cursor.execute("UPDATE cart SET total = ? WHERE Id_cart = ?", (total, cart_id))
    cursor.execute("UPDATE order_ SET total_amount = ? WHERE Id_order = ?", (total, order_id))

    # Étape 5 : Lier à un client
    user_id = 98
    cursor.execute("INSERT OR IGNORE INTO user_ (Id_user, username, email, password, user_type, vip) VALUES (?, ?, ?, ?, ?, ?)",
                   (user_id, 'testuser', 'test@example.com', 'hashed_password', 'customer', False))

    cursor.execute("INSERT INTO customer (Id_user, address, Id_order, Id_cart) VALUES (?, ?, ?, ?)",
                   (user_id, shipping_address, order_id, cart_id))

    conn.commit()
    conn.close()

    print("Test de création de panier terminé avec succès.")

if __name__ == "__main__":
    test_create_cart()
