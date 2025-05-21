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
    CREATE TABLE IF NOT EXISTS category(
        Id_category INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product(
        Id_product INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price REAL NOT NULL,
        stock_qty REAL,
        Id_category INTEGER NOT NULL,
        FOREIGN KEY(Id_category) REFERENCES category(Id_category)
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

    # Insertion des catégories
    cursor.executescript("""
    INSERT INTO category (name, description) VALUES
    ('Route', 'Vélos légers pour la route et la compétition'),
    ('VTT', 'Vélos tout terrain pour chemins et sentiers'),
    ('Électrique', 'Vélos avec assistance électrique'),
    ('Urbain', 'Vélos pour les trajets en ville'),
    ('Pliant', 'Vélos compacts et pliables'),
    ('Gravel', 'Vélos polyvalents route/chemin'),
    ('Enfant', 'Vélos adaptés aux enfants'),
    ('Cargo', 'Vélos pour transport de charges'),
    ('BMX', 'Vélos pour figures et skatepark'),
    ('Trekking', 'Vélos pour longues randonnées');
    """)

    # Insertion des produits avec liaison aux catégories
    cursor.executescript("""
    INSERT INTO product (name, description, price, stock_qty, Id_category) VALUES
    ('Vélo de route Canyon Ultimate', 'Cadre carbone, Shimano Ultegra', 2899.99, 12, 1),
    ('Vélo route Giant TCR Advanced', 'Cadre léger, Shimano 105', 2299.00, 8, 1),
    ('VTT Rockrider XC 500', 'Suspension avant, 12 vitesses', 999.90, 20, 2),
    ('VTT Trek Marlin 7', 'Cadre alu, freins à disque', 849.90, 15, 2),
    ('Vélo électrique Moustache Lundi 27', 'Batterie Bosch, confort urbain', 3199.00, 8, 3),
    ('Vélo électrique Cowboy 4', 'Design épuré, moteur intégré', 2499.00, 6, 3),
    ('Vélo urbain Elops 500', 'Style hollandais, 6 vitesses', 329.99, 18, 4),
    ('Vélo urbain Electra Loft 7D', 'Guidon droit, confortable', 599.00, 10, 4),
    ('Vélo pliant Brompton M6L', '6 vitesses, compact et léger', 1749.00, 15, 5),
    ('Vélo pliant Tilt 500', 'Facile à plier, léger', 379.99, 12, 5),
    ('Gravel Trek Checkpoint ALR 5', 'Polyvalent, Shimano GRX', 2399.50, 10, 6),
    ('Vélo gravel Cannondale Topstone', 'Freins à disque, pneus larges', 1999.00, 9, 6),
    ('Vélo enfant BTWIN 16 pouces', 'Pour enfants de 4 à 6 ans', 129.99, 25, 7),
    ('Vélo enfant Orbea MX 20', 'Confort et légèreté', 299.00, 14, 7),
    ('Vélo cargo Yuba Kombi', 'Transport familial ou marchandises', 1799.90, 6, 8),
    ('Vélo cargo Douze G4', 'Modulable, grande capacité', 3499.00, 4, 8),
    ('Vélo BMX Mongoose L20', 'Parfait pour skatepark et tricks', 349.95, 14, 9),
    ('Vélo BMX Sunday Primer', 'Cadre renforcé, freestyle', 459.99, 10, 9),
    ('Vélo trekking Riverside 920', 'Randonnée longue distance', 749.90, 9, 10),
    ('Vélo trekking KTM Life Track', 'Dérailleur Shimano, confort optimal', 899.00, 7, 10);
    """)

    conn.commit()
    conn.close()
    print("✅ Base de données corrigée et remplie avec catégories & produits liés.")
