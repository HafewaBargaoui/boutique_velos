import streamlit as st
from services.product_services import ProductService
from utils.style import set_style   


st.set_page_config(page_title="Mon panier", page_icon="🛒")

if st.button("Retour à l'accueil"):
    st.switch_page("main.py") 

st.title("🛒 Mon panier")

set_style()

# Initialiser le panier dans la session si besoin
if "cart" not in st.session_state:
    st.session_state.cart = []

# Supprimer un article du panier
def remove_item(index):
    st.session_state.cart.pop(index)
    st.experimental_rerun()

# Modifier la quantité d'un article
def update_quantity(index, qty):
    if qty > 0:
        st.session_state.cart[index]['qty'] = qty
    else:
        remove_item(index)

if not st.session_state.cart:
    st.info("Votre panier est vide.")
else:
    total = 0
    for index, item in enumerate(st.session_state.cart):
        product = ProductService.get_product_by_id(item['id_product'])
        if not product:
            continue

        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

        with col1:
            st.markdown(f"**{product.name}**<br>{product.price:.2f} €", unsafe_allow_html=True)

        with col2:
            new_qty = st.number_input(
                "Quantité",
                min_value=1,
                value=item['qty'],
                step=1,
                key=f"qty_{index}"
            )
            if new_qty != item["qty"]:
                update_quantity(index, new_qty)

        subtotal = product.price * item['qty']
        total += subtotal

        with col3:
            st.markdown(f"Sous-total : {subtotal:.2f} €")

        with col4:
            if st.button("❌", key=f"remove_{index}"):
                remove_item(index)

    st.markdown("---")
    st.markdown(f"### Total : {total:.2f} €")

    if st.button("🧾 Valider votre commande"):
        st.session_state.checkout_ready = True
        st.switch_page("pages/checkout.py")
