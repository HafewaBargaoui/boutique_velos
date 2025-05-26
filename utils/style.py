import streamlit as st

def set_style():
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none
        } 
        [data-testid="stSidebarCollapsedControl"] {
            display: none
        } 
        /* Fond clair de la page */
        [data-testid="stAppViewContainer"] {
            background-color: #f5f5f5;
        }

        /* Typographie générale */
        body, p, h1, h2, h3, h4 {
            color: #222;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Carte produit */
        .product-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 16px;
            margin-top: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
        }

        .product-card h4 {
            color: #333;
            font-size: 1.2em;
        }

        .product-price {
            display: inline-block;
            margin: 10px 0;
            padding: 6px 14px;
            border-radius: 6px;
            background-color: #10b981;
            color: white;
            font-weight: bold;
        }

        .product-stock {
            font-size: 0.9em;
            color: #555;
        }

        a.button-link {
            display: inline-block;
            margin-top: 10px;
            padding: 8px 16px;
            background-color: #e63946;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
        }
                
        .product-card-full {
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            padding: 0px;
            margin-top: 10px;
            text-align: center;
            overflow: hidden;
                
        }
        
        img {
             margin-bottom: 0;
            display: block;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            }


    </style>
    """, unsafe_allow_html=True)
