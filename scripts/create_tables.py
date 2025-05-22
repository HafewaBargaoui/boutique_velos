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
        Id_category INTEGER,
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS image(
        Id_image INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT,
        Id_product INTEGER,
        FOREIGN KEY(Id_product) REFERENCES product(Id_product)
    );
    """)

    # Insertion des catégories
    cursor.executescript("""
        INSERT INTO category (name, description) VALUES
        ('Route', 'Vélos de route rapides et légers'),
        ('VTT', 'Vélos tout terrain robustes'),
        ('Electrique', 'Vélos à assistance électrique'),
        ('Urbain', 'Vélos pour usage en ville'),
        ('Pliant', 'Vélos pliants compacts'),
        ('Gravel', 'Vélos polyvalents pour route et chemins'),
        ('Enfant', 'Vélos pour enfants'),
        ('Cargo', 'Vélos pour transport de charges'),
        ('BMX', 'Vélos pour acrobaties et skateparks'),
        ('Trekking', 'Vélos pour randonnée longue distance');

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

        INSERT INTO cart (total) VALUES
        (5799.98),
        (2199.90),
        (2899.00),
        (3499.00),
        (1599.00),
        (899.99),
        (399.00),
        (3400.00),
        (3299.00),
        (1749.00);

        INSERT INTO order_ (order_date, status, total_amount, shipping_adress) VALUES
        ('2024-05-01', 'delivered', 5799.98, '123 rue Exemple, Paris'),
        ('2024-05-02', 'shipped', 2199.90, '456 avenue Exemple, Lyon'),
        ('2024-05-03', 'pending', 2899.00, '789 boulevard Exemple, Marseille'),
        ('2024-05-04', 'delivered', 3499.00, '147 rue Exemple, Toulouse'),
        ('2024-05-05', 'delivered', 1599.00, '258 avenue Exemple, Nantes'),
        ('2024-05-06', 'cancelled', 899.99, '369 boulevard Exemple, Lille'),
        ('2024-05-07', 'delivered', 399.00, '741 rue Exemple, Bordeaux'),
        ('2024-05-08', 'delivered', 3400.00, '852 avenue Exemple, Strasbourg'),
        ('2024-05-09', 'pending', 3299.00, '963 boulevard Exemple, Nice'),
        ('2024-05-10', 'shipped', 1749.00, '357 rue Exemple, Grenoble');

        INSERT INTO customer (Id_user, address, Id_order, Id_cart) VALUES
        (1, '123 rue Exemple, Paris', 1, 1),
        (2, '456 avenue Exemple, Lyon', 2, 2),
        (3, '789 boulevard Exemple, Marseille', 3, 3),
        (4, '147 rue Exemple, Toulouse', 4, 4),
        (5, '258 avenue Exemple, Nantes', 5, 5),
        (6, '369 boulevard Exemple, Lille', 6, 6),
        (7, '741 rue Exemple, Bordeaux', 7, 7),
        (8, '852 avenue Exemple, Strasbourg', 8, 8),
        (9, '963 boulevard Exemple, Nice', 9, 9),
        (10, '357 rue Exemple, Grenoble', 10, 10);

        INSERT INTO cart_item (Id_cart, Id_order, Id_product, subtotal, qty) VALUES
        (1, 1, 1, 5799.98, 2),
        (2, 2, 3, 999.90, 1),
        (2, 2, 13, 129.99, 1),
        (3, 3, 5, 3199.00, 1),
        (4, 4, 9, 1749.00, 1),
        (4, 4, 11, 2399.50, 1),
        (5, 5, 2, 2299.00, 1),
        (6, 6, 4, 849.90, 1),
        (7, 7, 14, 299.00, 1),
        (8, 8, 20, 459.99, 1),
        (9, 9, 19, 899.00, 1),
        (10, 10, 9, 1749.00, 1);
                         
        INSERT INTO image (path, Id_product) VALUES
        ('assets/all_road_siver_bullet.jpg', 1),
        ('assets/all_road_siver_bullet.jpg', 2),
        ('assets/all_road_siver_bullet.jpg', 3),
        ('assets/all_road_siver_bullet.jpg', 4),
        ('assets/all_road_siver_bullet.jpg', 5),
        ('assets/all_road_siver_bullet.jpg', 6),
        ('assets/all_road_siver_bullet.jpg', 7),
        ('assets/all_road_siver_bullet.jpg', 8),
        ('assets/all_road_siver_bullet.jpg', 9),
        ('assets/all_road_siver_bullet.jpg', 10),
        ('assets/all_road_siver_bullet.jpg', 11),
        ('assets/all_road_siver_bullet.jpg', 12),
        ('assets/all_road_siver_bullet.jpg', 13),
        ('assets/all_road_siver_bullet.jpg', 14),
        ('assets/all_road_siver_bullet.jpg', 15),
        ('assets/all_road_siver_bullet.jpg', 16),
        ('assets/all_road_siver_bullet.jpg', 17),
        ('assets/all_road_siver_bullet.jpg', 18),
        ('assets/all_road_siver_bullet.jpg', 19),
        ('assets/all_road_siver_bullet.jpg', 20);                           
        """)

    conn.commit()
    conn.close()
    print("✅ Base de données corrigée et remplie avec catégories & produits liés.")
