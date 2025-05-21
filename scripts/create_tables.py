import sqlite3
import os

def create_tables():
    conn = sqlite3.connect("databases/ecommerce.db")
    cursor = conn.cursor()

    # Création des tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_(
        Id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        user_type TEXT NOT NULL,
        vip BOOLEAN NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin(
        Id_user INTEGER PRIMARY KEY,
        FOREIGN KEY(Id_user) REFERENCES user_(Id_user)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS super_admin(
        Id_user INTEGER PRIMARY KEY,
        FOREIGN KEY(Id_user) REFERENCES admin(Id_user)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart(
        Id_cart INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_(
        Id_order INTEGER PRIMARY KEY AUTOINCREMENT,
        order_date TEXT,
        status TEXT,
        total_amount REAL NOT NULL,
        shipping_adress TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product(
        Id_product INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price REAL NOT NULL,
        stock_qty REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS category(
        Id_category INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT,
        Id_product INTEGER NOT NULL,
        FOREIGN KEY(Id_product) REFERENCES product(Id_product)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer(
        Id_user INTEGER PRIMARY KEY,
        address TEXT NOT NULL,
        Id_order INTEGER NOT NULL,
        Id_cart INTEGER NOT NULL UNIQUE,
        FOREIGN KEY(Id_user) REFERENCES user_(Id_user),
        FOREIGN KEY(Id_order) REFERENCES order_(Id_order),
        FOREIGN KEY(Id_cart) REFERENCES cart(Id_cart)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart_item(
        Id_cart INTEGER,
        Id_order INTEGER,
        Id_product INTEGER,
        subtotal TEXT,
        qty TEXT,
        PRIMARY KEY(Id_cart, Id_order, Id_product),
        FOREIGN KEY(Id_cart) REFERENCES cart(Id_cart),
        FOREIGN KEY(Id_order) REFERENCES order_(Id_order),
        FOREIGN KEY(Id_product) REFERENCES product(Id_product)
    );
    """)

    # Insertion des produits exemple
    cursor.executescript("""
    INSERT INTO product (name, description, price, stock_qty) VALUES
    ('Vélo de route Canyon Ultimate', 'Cadre carbone, Shimano Ultegra', 2899.99, 12),
    ('VTT Rockrider XC 500', 'Suspension avant, 12 vitesses', 999.90, 20),
    ('Vélo électrique Moustache Lundi 27', 'Batterie Bosch, confort urbain', 3199.00, 8),
    ('Vélo pliant Brompton M6L', '6 vitesses, compact et léger', 1749.00, 15),
    ('Gravel Trek Checkpoint ALR 5', 'Polyvalent, Shimano GRX', 2399.50, 10),
    ('Vélo enfant BTWIN 16 pouces', 'Pour enfants de 4 à 6 ans', 129.99, 25),
    ('Vélo urbain Elops 500', 'Style hollandais, 6 vitesses', 329.99, 18),
    ('Vélo cargo Yuba Kombi', 'Transport familial ou marchandises', 1799.90, 6),
    ('Vélo BMX Mongoose L20', 'Parfait pour skatepark et tricks', 349.95, 14),
    ('Vélo trekking Riverside 920', 'Randonnée longue distance', 749.90, 9);
    """)

    conn.commit()
    conn.close()
    print("✅ Base de données et données d'exemple créées.")

