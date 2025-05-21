import sqlite3

def create_tables():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()

    #utilisateurs
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

    #admins
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin(
        Id_user INTEGER PRIMARY KEY,
        FOREIGN KEY(Id_user) REFERENCES user_(Id_user)
    );
    """)

    #admins
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS super_admin(
        Id_user INTEGER PRIMARY KEY,
        FOREIGN KEY(Id_user) REFERENCES admin(Id_user)
    );
    """)

    #panier
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart(
        Id_cart INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL
    );
    """)

    #commandes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_(
        Id_order INTEGER PRIMARY KEY AUTOINCREMENT,
        order_date TEXT,
        status TEXT,
        total_amount REAL NOT NULL,
        shipping_adress TEXT NOT NULL
    );
    """)

    #produits
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product(
        Id_product INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price REAL NOT NULL,
        stock_qty REAL
    );
    """)

    #catégories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS category(
        Id_category INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT,
        Id_product INTEGER NOT NULL,
        FOREIGN KEY(Id_product) REFERENCES product(Id_product)
    );
    """)

    #Clients
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

    #panier
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

    conn.commit()
    conn.close()
    print("Tables créées avec succès")

if __name__ == "__main__":
    create_tables()
