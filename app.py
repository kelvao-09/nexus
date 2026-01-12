import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")
if 'h' not in st.session_state: st.session_state.h = []

# 1. O GATINHO ELABORADO (Injeção via Componente)
st.components.v1.html("""
<div id="oneko" style="position:fixed; z-index:9999; pointer-events:none;"></div>
<script src="https://raw.githack.com/adryd325/oneko.js/master/oneko.js"></script>
<script>
    // Força o início do gatinho após o carregamento
    window.onload = function() { oneko.init(); };
</script>
""", height=0)

# 2. DESIGN E BOLA 🔮
st.markdown("""<style>
@keyframes mv {0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
.flt {font-size:70px;text-align:center;animation:mv 3s infinite;}
</style>""", unsafe_allow_html=True)

@st.cache_resource
def get_s():
    try:
        if "google_auth" in st.secrets:
            a = st.secrets["google_auth"]
            c = service_account.Credentials.from_service_account_info(a, scopes=['https://www.googleapis.com/auth/drive.readonly'])
            return build('drive', 'v3', credentials=c)
    except: return None
    return None

s = get_s()
st.markdown('<div class="flt">🔮</div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>O Oráculo</h2>", unsafe_allow_html=True)

# 3. BUSCA E HISTÓRICO (Linhas curtas para evitar o erro de sintaxe)
c1, c2, c
