import streamlit as st

def set_custom_style():
    st.markdown("""
        <style>
            body { background-color: #f4f4f4; color: #333; font-family: 'Segoe UI', sans-serif; }
            .main-title { font-size: 2.5em; font-weight: bold; color: #2296f3; margin-bottom: 0.5em; }
            .product-card {
                background: white; border-radius: 12px; padding: 1em;
                box-shadow: 0 4px 8px rgba(0,0,0,0.07); margin-bottom: 2em;
            }
            .product-title { font-size: 1.3em; font-weight: 600; }
            .product-price { color: #2296f3; font-weight: bold; font-size: 1.2em; }
        </style>
    """, unsafe_allow_html=True)
