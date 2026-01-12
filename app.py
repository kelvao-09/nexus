import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")

# Gatinho Gamer: Clique e use as SETAS
st.markdown("""
<div id="g" tabindex="0" style="position:fixed;bottom:20px;right:20px;font-size:60px;z-index:9999;outline:none;cursor:pointer;">🐈‍⬛</div>
<script>
const e=document.getElementById('g');let x=0,y=0;
e.onclick=()=>{e.focus();};
e.onkeydown=(k)=>{
 if(k.key=='ArrowUp')y-=30;if(k.key=='ArrowDown')y+=30;
 if(k.key=='ArrowLeft')x-=30;if(k.key=='ArrowRight')x+=30;
 e.style.transform=`translate(${x}px,${y}px)`;k.preventDefault();
};
</script>
<style>@keyframes f{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}.b{font-size:70px;text-align:center;animation:f 3s infinite;}</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_s():
 if "google_auth" in st.secrets:
  # Linhas curtas para evitar o corte do servidor
  s = ['https://www.googleapis.com/auth/drive.readonly']
  info = st.secrets["google_auth"]
  creds = service_account.Credentials.from_service_account_info(info, scopes=s)
  return build('drive', 'v3', credentials=creds)
 return None

srv = get_s()
st.markdown('<div class="b">🔮</div><h2 style="text-align:center;">Oráculo</h2>', unsafe_allow_html=True)
q = st.text_input("S", placeholder="Busque aqui...", label_visibility="collapsed")

if q and srv:
 try:
  filt = f"name contains '{q}' and trashed=false"
