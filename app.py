import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração da Página e Estilo CSS Personalizado
st.set_page_config(page_title="Oráculo Pro", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    /* Fundo e Container Principal */
    .main {
        background-color: #f0f2f6;
    }
    
    /* Estilização dos Cards */
    .doc-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.2s ease-in-out;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .doc-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #4285F4;
    }

    .doc-info {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .doc-icon {
        font-size: 2.5rem;
    }

    .btn-open {
        background-color: #4285F4;
        color: white !important;
        padding: 10px 25px;
        border-radius
