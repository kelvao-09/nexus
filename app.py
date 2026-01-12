import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")

# Interface de Controle do Gatinho
st.sidebar.markdown("### 🎮 Controle o Gato")
x = st.sidebar.slider("Horizontal", -100, 1500, 1200)
y = st.sidebar.slider("Vertical", -100, 800, 600)

# CSS para posicionar o gatinho conforme os sliders
st.markdown(f"""
<style>
    .cat-player {{
        position: fixed;
        left: {x}px;
        top: {y}px;
        font-size: 60px;
        z-index: 9999;
        transition: 0.2s ease-out;
        pointer-events: none;
    }}
    @keyframes f {{0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-15px)}}}}
    .b {{font-size:70px;text-align:center;animation:f 3s infinite;}}
</style>
<div class="cat-player">🐈‍⬛</div>
""", unsafe_allow_html=True)

@st.cache_resource
def get_s():
    if "google_auth" in st.secrets:
        return build('drive','v3',credentials=service_account.Credentials.from_service_account_info(st.secrets["google_auth"],scopes=['https://www.googleapis.com/auth/drive.readonly']))
    return None

s = get_s()
st.markdown('<div class="b">🔮</div><h2 style="text-align:center;">Oráculo</h2>', unsafe_allow_html=True)
q = st.text_input("S", placeholder="Busque aqui...", label_visibility="collapsed")

if q and s:
    try:
        r = s.files().list(q=f"name contains '{q}' and trashed=false", fields="files(name,webViewLink,mimeType)").execute().get('files', [])
        for i in r:
            if 'folder' not in i['mimeType']: st.markdown(f"📄 **[{i['name']}]({i['webViewLink']})**")
    except: st.error("!")
