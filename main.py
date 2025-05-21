import os
from scripts.create_tables import create_tables

# Crée la base de données une seule fois au démarrage
if not os.path.exists("databases/ecommerce.db"):
    create_tables()
import streamlit as st
from services.product_services import get_top_products
from utils.style import set_custom_style

# Crée ma page d'acceuil
st.set_page_config(page_title="Accueil | Boutique Vélos", layout="wide")
set_custom_style()

st.markdown("<div class='main-title'> Boutique de Vélos – Produits Populaires</div>", unsafe_allow_html=True)

produits = get_top_products(limit=3)

cols = st.columns(3)

for col, p in zip(cols, produits):
    with col:
        st.markdown(f"""
        <div class='product-card'>
            <div class='product-title'>{p.name}</div>
            <p>{p.description}</p>
            <div class='product-price'>{p.price} €</div>
            <p> Stock : {int(p.stock_qty)}</p>
        </div>
        """, unsafe_allow_html=True)
        
