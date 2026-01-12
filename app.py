import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configurações Iniciais
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")
if 'h' not in st.session_state: st.session_state.h = []

# 2. Código do Gatinho (JavaScript + CSS)
# Usando uma versão moderna do script "Oneko" que cria o gatinho seguidor
st.components.v1.html("""
<script src="https://raw.githubusercontent.com/adryd325/oneko.js/master/oneko.js"></script>
<script>
    // O script acima injeta o gato automaticamente. 
    // Ele vai perseguir o ponteiro do mouse por toda a tela do Oráculo.
</script>
<style>
    /* Estilo para garantir que o gato não atrapalhe os cliques nos botões */
    #oneko { pointer-events: none; z-index: 9999; }
</style>
""", height=0)

# 3. CSS do App (Animação da Bola 🔮)
st.markdown("""
<style>
    @keyframes mv {0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
    .flt {font-size:70px;text-align:center;animation:mv 3s infinite;}
    .card {background:white;padding:12px;border-radius:10px;border:1px solid #EEE;margin-bottom:8px;}
</style>
""", unsafe_allow_html=True)

# 4. Conexão Google Drive
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

# 5. Interface do Usuário
st.markdown('<div class="flt">🔮</div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>O Oráculo</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    q_in = st.text_input("S", placeholder="O que busca hoje?", label_visibility="collapsed")
    if st.session_state.h:
        cols = st.columns(len(st.session_state.h) + 1)
        for i, t in enumerate(st.session_state.h):
            if cols[i].button(t, key=f"h{i}"): q_in = t
        if cols[-1].button("🗑️"):
            st.session_state.h = []; st.rerun()

if q_in and q_in not in st.session_state.h
