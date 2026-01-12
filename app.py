import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")

# CSS: Gatinho com animação de balanço e Bola 🔮
st.markdown("""<style>
@keyframes tail { 0%,100%{transform:rotate(0deg)} 50%{transform:rotate(10deg) translateX(5px)} }
.cat{position:fixed;bottom:20px;right:20px;font-size:60px;z-index:999;animation:tail 2s infinite ease-in-out;}
@keyframes f{0%,100%{transform:translateY(0)} 50%{transform:translateY(-20px)}}
.b{font-size:75px;text-align:center;animation:f 3s infinite;margin-top:20px;}
</style><div class="cat">🐈‍⬛</div>""",unsafe_allow_html=True)

@st.cache_resource
def get_s():
    if "google_auth" in st.secrets:
        creds=service_account.Credentials.from_service_account_info(st.secrets["google_auth"],scopes=['https://www.googleapis.com/auth/drive.readonly'])
        return build('drive','v3',credentials=creds)
    return None

s=get_s()
st.markdown('<div class="b">🔮</div><h2 style="text-align:center;">Oráculo</h2>',unsafe_allow_html=True)
q=st.text_input("S",placeholder="O que busca?",label_visibility="collapsed")

if q and s:
    try:
        f_q=f"name contains '{q}' and mimeType!='application/vnd.google-apps.folder' and trashed=false"
        res=s.files().list(q=f_q,fields="files(name,webViewLink)").execute()
        files=res.get('files',[])
