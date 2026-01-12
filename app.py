import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
st.set_page_config(page_title="Oráculo", layout="wide")

# CSS em linha única para evitar o erro de corte do servidor
st.markdown('<style>@keyframes rato {0%{top:10%;left:10%;transform:scale(0.5);}25%{top:80%;left:30%;transform:scale(1.2);}50%{top:20%;left:80%;transform:scale(0.6);}75%{top:70%;left:60%;transform:scale(1.1);}100%{top:10%;left:10%;transform:scale(0.5);}}@keyframes gato {0%{top:15%;left:5%;transform:scale(0.6);}25%{top:85%;left:25%;transform:scale(1.3);}50%{top:25%;left:75%;transform:scale(0.7);}75%{top:75%;left:55%;transform:scale(1.2);}100%{top:15%;left:5%;transform:scale(0.6);}}.rat{position:fixed;font-size:30px;animation:rato 7s linear infinite;z-index:99;}.cat{position:fixed;font-size:45px;animation:gato 7s linear infinite;z-index:100;}@keyframes f{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}.b{font-size:70px;text-align:center;animation:f 3s infinite;}</style><div class="rat">🐭</div><div class="cat">🐈‍⬛</div>', unsafe_allow_html=True)

@st.cache_resource
def get_s():
 if "google_auth" in st.secrets:
  return build('drive','v3',credentials=service_account.Credentials.from_service_account_info(st.secrets["google_auth"],scopes=['https://www.googleapis.com/auth/drive.readonly']))
 return None
s=get_s()
st.markdown('<div class="b">🔮</div><h2 style="text-align:center;">Oráculo</h2>',unsafe_allow_html=True)
q=st.text_input("S",placeholder="Busque...",label_visibility="collapsed")
if q and s:
 r=s.files().list(q=f"name contains '{q}' and trashed=false",fields="files(name,webViewLink,mimeType)").execute().get('files',[])
 for i in r:
  if 'folder' not in i['mimeType']:st.markdown(f"📄 **[{i['name']}]({i['webViewLink']})**")
