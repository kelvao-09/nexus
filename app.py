import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")

# ESTE BLOCO MUDA O CURSOR PARA UM GATINHO
st.markdown("""
    <style>
        /* Define o gatinho como o cursor em toda a página */
        html, body, [data-testid="stAppViewContainer"] {
            cursor: url('https://cur.cursors-4u.net/anim/ani-11/ani1097.cur'), auto !important;
        }
        
        /* Garante que o gatinho apareça mesmo sobre botões e inputs */
        button, input, a, span {
            cursor: url('https://cur.cursors-4u.net/anim/ani-11/ani1097.cur'), pointer !important;
        }

        @keyframes flutua { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
        .bola { font-size: 70px; text-align: center; animation: flutua 3s infinite; }
    </style>
""", unsafe_allow_html=True)

# 2. CONEXÃO DRIVE
@st.cache_resource
def g_srv():
    try:
        if "google_auth" in st.secrets:
            s = st.secrets["google_auth"]
            c = service_account.Credentials.from_service_account_info(s, scopes=['https://www.googleapis.com/auth/drive.readonly'])
            return build('drive', 'v3', credentials=c)
    except: return None
    return None

srv = g_srv()

# 3. INTERFACE
st.markdown('<div class="bola">🔮</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>O Oráculo</h1>", unsafe_allow_html=True)

if 'h' not in st.session_state: st.session_state.h = []
q = st.text_input("Busca", placeholder="O que busca?", label_visibility="collapsed")

if q:
    if q not in st.session_state.h:
        st.session_state.h.insert(0, q)
        st.session_state.h = st.session_state.h[:5]
    
    if srv:
        try:
            filt = f"name contains '{q}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
            res = srv.files().list(q=filt, fields="files(name, webViewLink)").execute()
            for f in res.get('files', []):
                st.markdown(f"📄 **[{f['name']}]({f['webViewLink']})**")
        except: st.error("Erro na busca.")
