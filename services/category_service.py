import sqlite3


DB_PATH = "databases/ecommerce.db"

class CategoryService:

    def get_category_name_by_id(category_id):
        """
        Récupère le nom d'une catégorie à partir de son ID en interrogeant la base de données.
        """
        conn = sqlite3.connect(DB_PATH) 
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM category WHERE id_category = ?", (category_id,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            return "Catégorie inconnue"
