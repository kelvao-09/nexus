import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")

# Gatinho: Clique nele e use as SETAS do teclado
st.markdown("""
<div id="c" tabindex="0" style="position:fixed;bottom:20px;right:20px;font-size:50px;z-index:999;outline:none;cursor:pointer;">🐈‍⬛</div>
<script>
const g=document.getElementById('c');let x=0,y=0;
g.onkeydown=(e)=>{
 if(e.key=='ArrowUp')y-=30;if(e.key=='ArrowDown')y+=30;
 if(e.key=='ArrowLeft')x-=30;if(e.key=='ArrowRight')x+=30;
 g.style.transform=`translate(${x}px,${y}px)`;e.preventDefault();
};
</script>
<style>@keyframes f{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}.b{font-size:70px;text-align:center;animation:f 3s infinite;}</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_s():
 if "google_auth" in st.secrets:
  return build('drive','v3',credentials=service_account.Credentials.from_service_account_info(st.secrets["google_auth"],scopes=['https://www.googleapis.com/auth/drive.readonly']))
 return None

s=get_s()
st.markdown('<div class="b">🔮</div><h2 style="text-align:center;">Oráculo</h2>',unsafe_allow_html=True)
q=st.text_input("S",placeholder="Busque...",label_visibility="collapsed")

if q and
