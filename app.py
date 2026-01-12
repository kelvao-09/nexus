import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")
if 'h' not in st.session_state: st.session_state.h = []

# Gatinho Elaborado que segue o mouse (Injeção Direta)
st.components.v1.html("""
<div id="cat" style="position:fixed;width:50px;height:50px;pointer-events:none;z-index:9999;transition:0.1s;">
    <img src="https://i.gifer.com/Vg7.gif" width="50">
</div>
<script>
    const cat = document.getElementById('cat');
    document.addEventListener('mousemove', (e) => {
        cat.style.left = (e.pageX + 10) + 'px';
        cat.style.top = (e.pageY + 10) + 'px';
    });
</script>
""", height=0)

st.markdown("""<style>
@keyframes mv {0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
.flt {font-size:70px;text-align:center;animation:mv 3s infinite;}
</style>""", unsafe_allow_html=True)

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
st.
