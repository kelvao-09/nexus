import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")

# O Gatinho com lógica de Foco e Movimento
st.markdown("""
<div id="g" tabindex="0" style="position:fixed;bottom:20px;right:20px;font-size:60px;z-index:9999;outline:none;cursor:pointer;transition:0.1s;">🐈‍⬛</div>
<script>
const el=document.getElementById('g');let x=0,y=0;
el.onkeydown=(e)=>{
 if(e.key=='ArrowUp')y-=30;if(e.key=='ArrowDown')y+=30;
 if(e.key=='ArrowLeft')x-=30;if(e.key=='ArrowRight')x+=30;
 el.style.transform=`translate(${x}px,${y}px)`;e.preventDefault();
};
// Garante que o clique mude o foco para o gatinho
el.onclick=()=>{el.focus();};
</script>
<style>@keyframes f{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}.b{font-size:70px;text-align:center;animation:f 3s infinite;}</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_s():
 if "google_auth" in st.secrets:
  return build('drive','v3',credentials=service_account.Credentials.from_service_account_info(st.secrets["google_auth"],scopes=['
