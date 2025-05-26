import streamlit as st
from PIL import Image
from services.product_services import ProductService
from services.category_service import CategoryService
from utils.style import set_style

st.set_page_config(page_title="Catalogue", layout="wide")
set_style()

query_params = st.query_params
raw_category = query_params.get("id_category", [None])[0]
id_category = int(raw_category) if raw_category and raw_category.isdigit() else None

if st.button("Retour à l'accueil"):
    st.switch_page("main.py") 

if id_category:
    products = ProductService.get_products_by_category(id_category)
    category_name = CategoryService.get_category_name_by_id(id_category)
    if products:
        st.title(f"Produits : {category_name}")
    else:
        st.title(f"Aucun produit dans la catégorie : {category_name}")
else:
    products = ProductService.get_all_products()
    st.title("Tous les produits")

if products:
    for i in range(0, len(products), 3):
        cols = st.columns(3)
        for col, product in zip(cols, products[i:i+3]):
            with col:
                try:
                    if product.path:
                        image = Image.open(product.path)
                        st.image(image, use_container_width=True)
                except FileNotFoundError:
                    st.warning(f"Image introuvable : {product.path}")

                st.markdown(f"""
                    <div class='product-card'>
                        <h4>{product.name}</h4>
                        <p>{product.description}</p>
                        <div class='product-price'>{product.price} €</div>
                        <p class='product-stock'>Stock : {product.stock_qty}</p>
                        <a class='button-link' href="/product?id={product.id_product}" target="_self">Voir le produit</a>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.warning("Aucun produit trouvé.")
