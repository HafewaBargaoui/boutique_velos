import streamlit as st
from models.cart import Cart

st.set_page_config(page_title="Commande", page_icon="✅")
from utils.style import set_style
set_style()


if st.button("Retour à l'accueil"):
    st.session_state.checkout_ready = False
    st.session_state.checkout_executed = False
    st.switch_page("main.py")


if "checkout_ready" not in st.session_state or not st.session_state.checkout_ready:
    st.warning("Accès non autorisé. Merci de passer par la page panier pour valider votre commande.")
    st.stop()

cart = Cart()

if "checkout_executed" not in st.session_state:
    success, message = cart.checkout()
    st.session_state.checkout_executed = True
    st.session_state.checkout_success = success
    st.session_state.checkout_message = message
else:
    success = st.session_state.checkout_success
    message = st.session_state.checkout_message


if success:
    st.title("✅ Commande confirmée")
    st.success(message)
    st.image("assets/ribery.png", caption="Merci patron !", use_container_width=True)
else:
    st.error(message)

if not success and st.button("Retour au panier"):
    st.session_state.checkout_ready = False
    st.session_state.checkout_executed = False
    st.switch_page("pages/cart.py")
