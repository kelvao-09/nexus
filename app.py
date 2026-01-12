import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")

# CSS PURO: Gatinho fixo na lateral e Bola flutuante
st.markdown("""
    <style>
        /* O Gatinho na lateral direita */
        .gatinho-fixo {
            position: fixed;
            right: -10px;
            bottom: 50px;
            font-size: 60px;
            z-index: 9999;
            transform: rotate(-15deg);
            filter: drop-shadow(2px 2px 5px rgba(0,0,0,0.2));
        }

        /* Animação da Bola 🔮 */
        @keyframes flutua { 
            0%, 100% { transform: translateY(0); } 
            50% { transform: translateY(-20px); } 
        }
        .bola { 
            font-size: 80px; 
            text-align: center; 
            animation: flutua 3s infinite; 
            margin-bottom: 20px;
        }

        /* Esconder menus do Streamlit para ficar limpo */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    
    <div class="gatinho-fixo">🐈‍⬛</div>
""", unsafe_allow_html=True)

# 2. CONEXÃO DRIVE
@st.cache_resource
def get_drive():
    try:
        if "google_auth" in st.secrets:
            info = st.secrets["google_auth"]
            creds = service_account.Credentials.from_service_account_info(info, scopes=['https://www.googleapis.com/auth/drive.readonly'])
            return build('drive', 'v3', credentials=creds)
    except: return None
    return None

drive_service = get_drive()

# 3. INTERFACE
st.markdown('<div class="bola">🔮</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>O Oráculo</h1>", unsafe_allow_html=True)

if 'h' not in st.session_state: st.session_state.h = []
busca = st.text_input("S", placeholder="O que busca?", label_visibility="collapsed")

if busca:
    if busca not in st.session_state.h:
        st.session_state.h.insert(0, busca)
        st.session_state.h = st.session_state.h[:5]
    
    if drive_service:
        try:
            q = f"name contains '{busca
