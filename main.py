import os
from scripts.create_tables import create_tables

# Crée la base de données une seule fois au démarrage
if not os.path.exists("databases/ecommerce.db"):
    create_tables()