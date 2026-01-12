import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração e Estilo
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")
if 'h' not in st.session_state: st.session_state.h = []

# CSS: Levitação da bola e o Gatinho Espião
st.markdown("""
<style>
    /* Animação da Bola 🔮 */
    @keyframes mv {0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
    .flt {font-size:70px;text-align:center;animation:mv 3s infinite;}

    /* Animação do Gatinho Espião 🐱 */
    @keyframes peek {
        0%, 90%, 100% { right: -50px; } /* Escondido */
        95% { right: 0px; } /* Espiando */
    }
    .cat-spy {
        position: fixed;
        bottom: 20%;
        right: -50px;
        font-family: monospace;
        font-size: 12px;
        color: #888;
        background: white;
        padding: 5px;
        border-radius: 5px 0 0 5px;
        border: 1px solid #EEE;
        animation: peek 20s infinite; /* Ele aparece a cada 20s para teste. Para 5min, mude para 300s */
        z-index: 999;
    }
</style>
<div class="cat-spy">
    |\\__/,|   <br>
    |o o  |   <br>
    _.( T )._ 
</div>
""", unsafe_allow_html=True)

# 2. Conexão Drive
@st.cache_resource
def get_s():
    try:
        if "google_auth" in st.secrets:
            auth = st.secrets["google_auth"]
            creds = service_account.Credentials.from_service_account_info(auth, scopes=['https://www.googleapis.com/auth/drive.readonly'])
            return build('drive', 'v3', credentials=creds)
    except: return None
    return None

s = get_s()

# 3. Interface Principal
st.markdown('<div class="flt">🔮</div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>O Oráculo</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    q_in = st.text_input("S", placeholder="O que busca?", label_visibility="collapsed")
    if st.session_state.h:
        cols = st.columns(len(st.session_state.h) + 1)
        for i, t in enumerate(st.session_state.h):
            if cols[i].button(t, key=f"h{i}"): q_in = t
        if cols[-1].button("🗑️"):
            st.session_state.h = []; st.rerun()

if q_in and q_in not in st.session_state.h:
    st.session_state.h.insert(0, q_in); st.session_state.h = st.session_state.h[:5]

# 4. Busca em linha única (Arquivos apenas)
if q_in and s:
    try:
        q = f"name contains '{q_in}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = s.files().list(q=q, fields="files(id, name, webViewLink)").execute()
        items = res.get('files', [])
        if items:
            st.write("---")
            for f in items:
                st.markdown(f"📄 **[{f['name']}]({f['webViewLink']})**")
        else: st.info("Nada encontrado.")
    except: st.error("Erro na busca.")
