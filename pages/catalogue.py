import os
import streamlit as st
from PIL import Image
from utils.style import set_style  # style clair
from services.product_services import ProductService

# Section Produits 
products = ProductService.get_all_products()

# Affichage par groupe de 3 produits (ligne par ligne)
for i in range(0, len(products), 3):
    cols = st.columns(3)
    for col, product in zip(cols, products[i:i+3]):
        with col:
            try:
                img = Image.open(product.path)
                st.image(img, use_container_width=True)
            except FileNotFoundError:
                st.warning(f"Image introuvable : {product.path}")
            st.markdown(f"""
                <div class='product-card'>
                    <h4>{product.name}</h4>
                    <p>{product.description}</p>
                    <div class='product-price'> {product.price} €</div>
                    <p class='product-stock'>Stock : {product.stock_qty}</p>
                    <a class='button-link' href="/product?id={product.id_product}" target="_self">Voir le produit</a>
                </div>
            """, unsafe_allow_html=True)
