import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")
if 'h' not in st.session_state: st.session_state.h = []

# CSS Minimalista Animado
st.markdown("""<style>
@keyframes mv {0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
.flt {font-size:70px;text-align:center;animation:mv 3s infinite;}
.stButton>button {border-radius:20px;padding:2px 10px;font-size:12px;}
</style>""", unsafe_allow_html=True)

# Conexão Drive
@st.cache_resource
def get_s():
    try:
        if "google_auth" in st.secrets:
            info = st.secrets["google_auth"]
            sc = ['https://www.googleapis.com/auth/drive.readonly']
            creds = service_account.Credentials.from_service_account_info(info, scopes=sc)
            return build('drive', 'v3', credentials=creds)
    except: return None
    return None

s = get_s()

# Interface
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
    st.session_state.h.insert(0, q_in)
    st.session_state.h = st.session_state.h[:5]

# Busca (Filtrada para ARQUIVOS apenas)
if q_in and s:
    try:
        query = f"name contains '{q_in}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = s.files().list(q=query,
