import streamlit as st
from services.product_admin_service import ProductAdminService

st.set_page_config(page_title="Admin - Gestion Catalogue", layout="wide")
st.title("🛠️ Administration du Catalogue")

# Choix de l'action
action = st.sidebar.radio("Actions", ["Gérer les Produits", "Voir les Commandes"])

# --- Produits ---
if action == "Gérer les Produits":
    st.header("📦 Gestion des Produits")
    produits = ProductAdminService.get_all_products()
    categories = ProductAdminService.get_all_categories()
    cat_dict = {cat.id_category: cat.name for cat in categories}

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Liste des produits existants")
        for prod in produits:
            with st.expander(f"{prod.name} - {prod.price} € (Stock: {prod.stock_qty})"):
                st.write(prod.description)
                st.write(f"Catégorie : {cat_dict.get(prod.id_category, 'Inconnue')}")

                if st.button("🗑 Supprimer", key=f"del_{prod.id_product}"):
                    ProductAdminService.delete_product(prod.id_product)
                    st.success("Produit supprimé.")
                    st.rerun()

    with col2:
        st.subheader("➕ Ajouter ou modifier un produit")
        selected_id = st.selectbox("Modifier un produit existant", [None] + [p.id_product for p in produits], format_func=lambda x: "Nouveau produit" if x is None else f"Produit ID {x}")
        selected_prod = next((p for p in produits if p.id_product == selected_id), None)

        name = st.text_input("Nom", value=selected_prod.name if selected_prod else "")
        description = st.text_area("Description", value=selected_prod.description if selected_prod else "")
        price = st.number_input("Prix (€)", min_value=0.0, value=selected_prod.price if selected_prod else 0.0)
        stock = st.number_input("Quantité en stock", min_value=0, value=selected_prod.stock_qty if selected_prod else 0)
        category = st.selectbox("Catégorie", cat_dict.items(), index=0 if not selected_prod else list(cat_dict).index(selected_prod.id_category))

        if st.button("💾 Enregistrer"):
            if selected_prod:
                ProductAdminService.update_product(selected_prod.id_product, name, description, price, stock, category[0])
                st.success("Produit mis à jour !")
            else:
                ProductAdminService.add_product(name, description, price, stock, category[0])
                st.success("Produit ajouté !")
            st.rerun()

# --- Commandes ---
elif action == "Voir les Commandes":
    st.header("📑 Commandes passées")
    orders = ProductAdminService.get_all_orders()

    if orders.empty:
        st.info("Aucune commande enregistrée.")
    else:
        for _, row in orders.iterrows():
            with st.expander(f"Commande #{row['id_order']} - {row['order_date']} - {row['username']} ({row['email']})"):
                st.write(f"📍 Adresse de livraison : {row['shipping_adress']}")
                st.write(f"💶 Total : {row['total_amount']} €")
                st.write(f"📦 Statut : {row['status']}")
                details = ProductAdminService.get_order_details(row['id_order'])
                st.table(details)
