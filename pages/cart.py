import streamlit as st
from models.cart import Cart

st.set_page_config(page_title="Votre panier", layout="wide")
from utils.style import set_style
set_style()

# Initialiser le panier dans la session si absent
if "cart" not in st.session_state:
    st.session_state.cart = {}

if st.button("Retour à l'accueil"):
    st.switch_page("main.py") 

cart = Cart()

st.title("Votre panier")

items = cart.get_items()

if not items:
    st.info("Votre panier est vide.")
else:
    st.write("Modifiez les quantités et cliquez sur Mettre à jour.")

    updated_qty = {}

    for item in items:
        pid = str(item["id_product"]) 

        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

        with col1:
            st.write(item["name"])
        with col2:
            st.write(f"{item['price']} €")
        with col3:
            qty = st.number_input(
                label=f"Quantité ({pid})",
                min_value=0,
                value=item["qty"],
                step=1,
                key=f"qty_{pid}"
            )
            updated_qty[pid] = qty
        with col4:
            st.write(f"{item['subtotal']} €")
        with col5:
            if st.button("Supprimer", key=f"del_{pid}"):
                cart.remove_product(pid)
                st.rerun()

    if st.button("Mettre à jour les quantités"):
        for pid, qty in updated_qty.items():
            if qty == 0:
                cart.remove_product(pid)
            else:
                st.session_state.cart[pid]["qty"] = qty
        st.success("Panier mis à jour.")
        st.rerun()

    total = cart.get_total()
    st.markdown(f"### Total : {total} €")

    if st.button("Vider le panier"):
        cart.clear_cart()
        st.rerun()

    if st.button("Finaliser votre commande"):
        if len(st.session_state.cart) == 0:
            st.warning("Votre panier est vide, impossible de finaliser la commande.")
        else:
            st.session_state.checkout_ready = True
            st.switch_page("pages/checkout.py") 
