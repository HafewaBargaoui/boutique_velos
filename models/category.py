import sqlite3
DB_PATH = "databases/ecommerce.db"
class Category:
    def __init__(self, name, description, id_category= None):
        self.id_category = id_category
        self.name = name
        self.description = description

    def add_category(self):
        try:
            if self.id_category is not None:
                print("L'ajout est bloqué : l'ID de la catégorie est déjà défini.")
                return

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO category (name, description)
                    VALUES (?, ?)
                """, (self.name, self.description))  
                self.id_category = cursor.lastrowid
                conn.commit()
                print(f"Catégorie ajoutée avec l'ID {self.id_category}")
        except sqlite3.IntegrityError:
            print(f"La catégorie '{self.name}' existe déjà.")
        except sqlite3.Error as e:
            print("Erreur SQLite :", e)