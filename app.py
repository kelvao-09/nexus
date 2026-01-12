import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuração e Estilo
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

if 'h' not in st.session_state:
    st.session_state.h = []

# CSS: Levitação da Bola e Estilo dos Cards
st.markdown("""
<style>
    @keyframes mv {0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
    .flt {font-size:70px;text-align:center;animation:mv 3s infinite;}
    .card {background:white;padding:12px;border-radius:10px;border:1px solid #EEE;margin-bottom:8px;}
    #oneko { position: fixed; z-index: 9999; pointer-events: none; }
</style>
""", unsafe_allow_html=True)

# 2. O Gatinho que Persegue o Mouse (JavaScript Interativo)
st.components.v1.html("""
<script>
(function() {
  const script = document.createElement('script');
  script.src = "https://raw.githubusercontent.com/adryd325/oneko.js/master/oneko.js";
  script.onload = () => { /* O gatinho inicia automaticamente ao carregar o script */ };
  document.head.appendChild(script);
})();
</script>
""", height=0)

# 3. Conexão Google Drive
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

# 4. Interface Principal
st.markdown('<div class="flt">🔮</div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>O Oráculo</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    q_in = st.text_input("Busca", placeholder="O que deseja encontrar?", label_visibility="collapsed")
    if st.session_state.h:
        cols = st.columns(len(st.session_state.h) + 1)
        for i, t in enumerate(st.session_state.h):
            if cols[i].button(t, key=f"h{i}"): q_in = t
        if cols[-1].button("🗑️"):
            st.session_state.h = []
            st.rerun()

# Lógica de Histórico Protegida contra SyntaxError
if q_in:
    if q_in not in st.session_state.h:
        st.session_state.
