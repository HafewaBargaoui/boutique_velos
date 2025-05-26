import streamlit as st
import os
from PIL import Image
from services.product_services import ProductService
from utils.style import set_style

st.set_page_config(page_title="Détail du produit", layout="wide")
set_style()

# Récupération de l'ID depuis l'URL
params = st.query_params
raw_id = params.get("id", [None])[0]
product_id = int(raw_id) if raw_id and raw_id.isdigit() else None

if not product_id:
    st.error("Aucun ID de produit fourni.")
    st.stop()

product = ProductService.get_product_by_id(product_id)

if not product:
    print(product_id)
    st.error("Produit introuvable.")
    st.stop()

if st.button("Retour à l'accueil"):
    st.switch_page("main.py") 

# Mise en page
st.title(product.name)

col1, col2 = st.columns([1, 2])

with col1:
    try:
        picture_path = ProductService.get_product_image_by_id(product.id_product)
        if picture_path and os.path.exists(picture_path):
            picture = Image.open(picture_path)
            st.image(picture, use_container_width=True)
        else:
            st.warning(f"Image introuvable pour le produit : {product.name}")
    except Exception as e:
        st.error(f"Erreur lors de l'ouverture de l'image : {e}")

with col2:
    st.markdown(f"""
        <div style='
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        '>
            <p><strong>Description :</strong> {product.description}</p>
            <p><strong>Prix :</strong> {product.price} €</p>
            <p><strong>Stock :</strong> {product.stock_qty}</p>
        </div>
    """, unsafe_allow_html=True)
