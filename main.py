import streamlit as st
from services.product_services import get_top_products
from utils.style import set_custom_style

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
        