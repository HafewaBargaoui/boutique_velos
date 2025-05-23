import streamlit as st
from utils.style import set_style


if st.button("Retour à l'accueil"):
    st.switch_page("main.py") 


st.set_page_config(page_title="Commande", page_icon="✅")

set_style()

if "checkout_ready" not in st.session_state or not st.session_state.checkout_ready:
    st.warning("Accès non autorisé. Merci de passer par la page panier pour valider votre commande.")
    st.stop()

st.title("✅ Commande confirmée")
st.success("Merci pour votre achat ! Votre commande a bien été enregistrée.")

# Réinitialisation du panier et de l'état
st.session_state.cart = []
st.session_state.checkout_ready = False
