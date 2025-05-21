import sqlite3

DB_PATH = "databases/ecommerce.db"

def get_best_selling_products(limit=5):
    """
    Retourne les produits les plus vendus dans la boutique.

    Args:
        limit (int): Nombre maximum de produits à retourner.

    Returns:
        List[Tuple[str, int]]: Liste de tuples (nom du produit, quantité totale vendue).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.name,
            SUM(CAST(ci.qty AS INTEGER)) AS total_sold
        FROM cart_item ci
        JOIN product p ON ci.Id_product = p.Id_product
        GROUP BY ci.Id_product
        ORDER BY total_sold DESC
        LIMIT ?;
    """, (limit,))

    results = cursor.fetchall()
    conn.close()
    return results
