import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")
if 'h' not in st.session_state: st.session_state.h = []

# Gatinho que segue o mouse SEM PARAR
st.components.v1.html("""
<div id="k" style="position:fixed;pointer-events:none;z-index:999;left:0;top:0;">
    <img src="https://i.gifer.com/Vg7.gif" width="50">
</div>
<script>
document.addEventListener('mousemove',(e)=>{
    const k=document.getElementById('k');
    k.style.transform = `translate(${e.clientX+5}px, ${e.clientY+5}px)`;
});
</script>""", height=0)

st.markdown("<style>@keyframes m{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}.f{font-size:60px;text-align:center;animation:m 3s infinite;}</style>", unsafe_allow_html=True)

@st.cache_resource
def get_s():
    if "google_auth" in st.secrets:
        return build('drive', 'v3', credentials=service_account.Credentials.from_service_account_info(st.secrets["google_auth"], scopes=['https://www.googleapis.com/auth/drive.readonly']))
    return None

s = get_s()
st.markdown('<div class="f">🔮</div><h2 style="text-align:center;">Oráculo</h2>', unsafe_allow_html=True)
q = st.text_input("S", placeholder="O que busca?", label_visibility="collapsed")

if q:
    if q not in st.session_state.h:
        st.session_state.h.insert(0
