import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
import PyPDF2

# Configs
ak, au = st.secrets.get("gemini_api"), st.secrets.get("google_auth")
if ak:
    genai.configure(api_key=ak)
    md = genai.GenerativeModel('gemini-1.5-flash')

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
                    mType = i.get('mimeType', '')
                    # 1. Se for Google Doc
                    if "google-apps.document" in mType:
                        m = s.files().export(fileId=i['id'], mimeType='text/plain').execute()
                        st.session_state.txt = m.decode('utf-8')
                    # 2. Se for PDF
                    elif "pdf" in mType:
                        m = s.files().get_media(fileId=i['id']).execute()
                        pdf_reader = PyPDF2.PdfReader(io.BytesIO(m))
                        texto_pdf = ""
                        for page in pdf_reader.pages:
                            texto_pdf += page.extract_text()
                        st.session_state.txt = texto_pdf
                    # 3. Se for TXT ou outro
                    else:
                        m = s.files().get_media(fileId=i['id']).execute()
                        st.session_state.txt = m.decode('utf-8')
                    
                    st.success("Lido com sucesso!")
                except Exception as e:
                    st.error(f"Erro: {e}")

with t2:
    if st.session_state.txt:
        p = st.chat_input("Dúvida sobre o documento?")
        if p:
            # Enviamos o texto como contexto para o Oráculo
            r = md.generate_content(f"Contexto: {st.session_state.txt[:10000]}\n\nPergunta: {p}")
            st.chat_message("assistant").write(r.text)
    else: st.warning("Leia um arquivo primeiro.")
