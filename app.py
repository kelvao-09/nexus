import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")
if 'h' not in st.session_state: st.session_state.h = []

# Injeção Direta de CSS e JS (Gatinho 🐈)
st.markdown("""
<div id="cat" style="position:fixed;pointer-events:none;z-index:9999;font-size:40px;left:0;top:0;">🐈</div>
<style>
    @keyframes m{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
    .f{font-size:60px;text-align:center;animation:m 3s infinite;}
</style>
<script>
    document.addEventListener('mousemove', function(e) {
        var cat = document.getElementById('cat');
        cat.style.transform = 'translate(' + (e.clientX + 10) + 'px, ' + (e.clientY + 10) + 'px)';
    });
</script>
""", unsafe_allow_html=True)

@st.cache_resource
def get_s():
    if "google_auth" in st.secrets:
        return build('drive', 'v3', credentials=service_account.Credentials.from_service_account_info(st.secrets["google_auth"], scopes=['https://www.googleapis.com/auth/drive.readonly']))
    return None

s, h = get_s(), st.session_state.h
st.markdown('<div class="f">🔮</div><h2 style="text-align:center;">Oráculo</h2>', unsafe_allow_html=True)
q = st.text_input("Busca", placeholder="O que busca?", label_visibility="collapsed")

if q:
    if q not in h: h.insert(0,q); st.session_state.h=h[:5]
    if s:
        try:
            filt = f"name contains '{q}' and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
            res = s.files().list(q=filt, fields="files(name, webViewLink)").execute()
            for f in res.get('files', []):
                st.markdown(f"📄 **[{f['name']}]({f['webViewLink']})**")
        except: st.error("Erro")
