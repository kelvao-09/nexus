import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
st.set_page_config(page_title="Oráculo", layout="wide")
# Gato e Rato em perseguição 100% CSS
st.markdown("""
<style>
@keyframes chase{0%{left:0%;top:0%;}25%{left:90%;top:0%;}50%{left:90%;top:90%;}75%{left:0%;top:90%;}100%{left:0%;top:0%;}}
.rat{position:fixed;width:30px;height:30px;animation:chase 10s linear infinite alternate;z-index:99;}
.cat{position:fixed;width:40px;height:40px;font-size:35px;animation:chase 10s linear infinite alternate-reverse;z-index:100;transform:scaleX(-1) translate(10px,10px);}
@keyframes f{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}.b{font-size:70px;text-align:center;animation:f 3s infinite;}
</style>
<div class="rat">🐭</div>
<div class="cat">🐈‍⬛</div>
""",unsafe_allow_html=True)
@st.cache_resource
def get_s():
 if "google_auth" in st.secrets:
  sc=['https://www.googleapis.com/auth/drive.readonly']
  return build('drive','v3',credentials=service_account.Credentials.from_service_account_info(st.secrets["google_auth"],scopes=sc))
 return None
s=get_s()
st.markdown('<div class="b">🔮</div><h2 style="text-align:center;">Oráculo</h2>',unsafe_allow_html=True)
q=st.text_input("S",placeholder="Busque...",label_visibility="collapsed")
if q and s:
 r=s.files().list(q=f"name contains '{q}' and trashed=false",fields="files(name,webViewLink,mimeType)").execute().get('files',[])
 for i in r:
  if 'folder' not in i['mimeType']:st.markdown(f"📄 **[{i['name']}]({i['webViewLink']})**")
