import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Oráculo", layout="wide")
# Gatinho Fixo e Bola 🔮
st.markdown("""<style>
.cat{position:fixed;top:10px;left:10px;font-size:50px;z-index:99}
@keyframes f{0%,100%{transform:translateY(0)}50%{transform:translateY(-20px)}}
.b{font-size:70px;text-align:center;animation:f 3s infinite}
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
        # Linha ultra curta para evitar corte
        f_q=f"name contains '{q}' and mimeType!='application/vnd.google-apps.folder' and trashed=false"
        res=s.files().list(q=f_q,fields="files(name,webViewLink)").execute()
        for f in res.get('files',[]):
            st.markdown(f"📄 **[{f['name']}]({f['webViewLink']})**")
    except:st.error("Erro")
