import os
import streamlit as st
from PIL import Image

from scripts.create_tables import create_tables
from utils.style import set_style  # style clair
from services.product_services import ProductService
from services.category_service import CategoryService

# Configuration de la page
st.set_page_config(page_title="Boutique de Vélos", layout="wide")

# Créer la base si elle n'existe pas
if not os.path.exists("databases/ecommerce.db"):
    create_tables()

# Appliquer le style clair
set_style()

# Affiche l'image de bannière
image = Image.open("assets/fond_pageacceuil.jpg")
st.image(image, use_container_width=True)

# Titre et bouton centré sur la bannière
st.markdown("""
<div style='
    text-align: center;
    margin-top: -300px;
    z-index: 1;
    position: relative;
'>
    <h1 style='color: #0d1a26; font-size: 3em; font-weight: bold;'>BOUTIQUE DE VÉLOS</h1>
    <a href="/catalogue" target="_self" style='
        padding: 12px 24px;
        background-color: #e63946;
        color: white;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.1em;
    '>Découvrir nos vélos</a>
</div>
""", unsafe_allow_html=True)

# Section Catégories

st.markdown("""
<h2 style='
    text-align: center;
    color: #000000;
    text-transform: uppercase;
    font-size: 2.2em;
    margin-top: 60px;
    margin-bottom: 20px;
'>
    Catégories de vélos
</h2>
""", unsafe_allow_html=True)

categories = ProductService.get_all_categories()

if categories:
    cat_cols = st.columns(len(categories))
    for col, cat in zip(cat_cols, categories):
        img = f"./assets/image_category/{cat.name}.png"
        with col:
            st.image(img)
            st.markdown(f"""
                <a href="/Catalogue?id_category={cat.id_category}" target="_self" style="text-decoration: none;">
                    <div style='
                        background-color: #ffffff;
                        border-radius: 14px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                        text-align: center;
                        padding: 16px;
                        transition: transform 0.2s ease;
                    '>
                        <h4 style="color: #111; margin-top: 12px;">{cat.name}</h4>
                    </div>
                </a>
            """, unsafe_allow_html=True)
else:
    st.warning("Aucune catégorie trouvée.")

# Espace après la bannière

st.markdown("<br><br><br><br>", unsafe_allow_html=True)

# Section Produits Populaires

st.markdown("""
<h1 style='
    text-align: center;
    color: #000000;
    font-size: 2.6em;
    margin-top: 40px;
    margin-bottom: 20px;
'>
    Best Sellers
</h1>
""", unsafe_allow_html=True)

products = ProductService.get_top_products()
cols = st.columns(3)

for col, product in zip(cols, products):
    with col:
        try:
            picture_path = ProductService.get_product_image_by_id(product.id_product)
            if picture_path and os.path.exists(picture_path):
                picture = Image.open(picture_path)
                st.image(picture, use_container_width=True)
            else:
                st.warning(f"Image introuvable pour le produit : {product.name}")
        except Exception as e:
            st.error(f"Erreur lors de l'ouverture de l'image : {e}")
        st.markdown(f"""
            <div class='product-card'>
                <h4>{product.name}</h4>
                <p>{product.description}</p>
                <div class='product-price'> {product.price} €</div>
                <p class='product-stock'>Stock : {product.stock_qty}</p>
                <a class='button-link' href="/product?id={product.id_product}" target="_self">Voir le produit</a>
            </div>
        """, unsafe_allow_html=True)


# Section Stock Limité

st.markdown("""
<h1 style='
    text-align: center;
    color: #000000;
    font-size: 2.6em;
    margin-top: 40px;
    margin-bottom: 20px;
'>
    Stock limité
</h1>
""", unsafe_allow_html=True)

products = ProductService.get_limited_stock_products()

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
            
#Gestion du panier
if "cart" not in st.session_state:
    st.session_state.cart = []
