import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io, PyPDF2

# --- CONFIGS ---
ak, au = st.secrets.get("gemini_api"), st.secrets.get("google_auth")
if ak: genai.configure(api_key=ak)

@st.cache_resource
def detectar_modelo():
    try:
        # Busca na sua conta quais modelos aceitam gerar conteúdo
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
    except: return None
    return None

modelo_valido = detectar_modelo()
if "txt" not in st.session_state: st.session_state.txt = ""

st.title("O Oráculo")
t1, t2 = st.tabs(["Busca", "Chat"])

with t1:
    q = st.text_input("Arquivo:")
    if q and au:
        c = service_account.Credentials.from_service_account_info(au, scopes=['https://www.googleapis.com/auth/drive.readonly'])
        s = build('drive', 'v3', credentials=c)
        res = s.files().list(q=f"name contains '{q}'").execute().get('files', [])
        for i in res:
            st.write(f"📄 {i['name']}")
            if st.button("Ler", key=i['id']):
                try:
                    tp = i.get('mimeType', '')
                    if "document" in tp:
                        m = s.files().export(fileId=i['id'], mimeType='text/plain').execute()
                    else:
                        m = s.files().get_media(fileId=i['id']).execute()
                    
                    if "pdf" in tp:
                        pdf = PyPDF2.PdfReader(io.BytesIO(m))
                        st.session_state.txt = "".join([p.extract_text() for p in pdf.pages])
                    else:
                        st.session_state.txt = m.decode('utf-8')
                    st.success(f"Lido! (IA: {modelo_valido})")
                except Exception as e: st.error(f"Erro: {e}")

with t2:
    if st.session_state.txt and modelo_valido:
        p = st.chat_input("Dúvida?")
        if p:
            try:
                md = genai.GenerativeModel(modelo_valido)
                r = md.generate_content(f"Doc: {st.session_state.txt[:8000]}\n\nPergunta: {p}")
                st.chat_message("assistant").write(r.text)
            except Exception as e: st.error(f"Erro na IA: {e}")
    elif not modelo_valido:
        st.error("Nenhum modelo compatível encontrado nesta chave API.")
    else: st.warning("Leia um arquivo primeiro.")
