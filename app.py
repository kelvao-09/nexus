import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="O Oráculo", layout="wide")

# --- 1. CONFIGURAÇÃO DA IA (GEMINI) ---
if "gemini_api" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["gemini_api"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        ia_ativa = True
    except Exception as e:
        st.error(f"Erro ao configurar Gemini: {e}")
        ia_ativa = False
else:
    st.error("Chave Gemini não encontrada. Verifique os Secrets.")
    ia_ativa = False

# --- 2. ANIMAÇÃO DVD BOUNCE ---
st.markdown('<style>@keyframes bX{0%{left:0}100%{left:calc(100% - 220px)}}@keyframes bY{0%{top:0}100%{top:calc(100% - 50px)}}.dvd{position:fixed;font-size:18px;font-weight:bold;color:#FFF;background:#000;padding:10px;z-index:999;animation:bX 7s linear infinite alternate,bY 5s linear infinite alternate;}</style><div class="dvd">Esperar é Caminhar</div>', unsafe_allow_html=True)

# --- 3. INTERFACE E CARICATURA ---
st.markdown('<h1 style="text-align:center;">O Oráculo</h1>', unsafe_allow_html=True)
st.image("https://lh3.googleusercontent.com/rd-gg-dl/ABS2GSmNEX0Dw0uBJnn9_Hu8tEI4Z14i4rC4Im0Ko5lZ9ojchlG4aV_wxRZ4UEr79bY8Mqaju8oxTGjO1fbO_WwXv4zZaFshmSnkQyh8ahM6ItEDyGh6fjLnJWP5mVyxPQAuBRz5w4GtPHb0fTG1OGTdDqfmbjlpT5angjjW4VyvNLUmnMgeR3ODazEesTwevvX0gpR3w9thS089Xr3hnJTLkaG1aslhVw1hlGYeGOmiRWtQmrmnsxPGMUTVH8PyoyKAuiKsHkGk1lJZ6140NI5BL7di1dcpMfVmsF2li_tkETXUfMNybqciC-p_zCMu38m7VRAym4yyjnCpym-kPCcM0vUED2e7GBodvQ41f97AauzrTFfNTIoaTtoqmLs-hPRi3Hp401ePE2Q7ZdBjPstoiBHqps5cUOeNMIj9mrj4MJC4Lp6n4CMkQDtVXxUAIjhMMaRTNDc6WGeueccUlm7ieu0BYPQE-SeuVHA1ghLPziVOua-2GOlFMsrWY-vmHkRHtgEBcDg4GsQU3bWbQFx_DaYq5_hmJ9SAi_EssTujs_Law3rFnEpHS59Xd-hVD2wbZL_CDsL1MXLk5_W_HpZJro2Xf1yfYw0lCo3Hd-cmZUu2EkbKRAWYpJx5IcqzUG5nWtpSODZ2TbwiGCgVcXVT55x9ae03NPB2IRWdGTSWm2Stx4q-JKSb38IRpOYdP40hZF5X8suxC0c4ZYbIUu9SvLyIJDuHjxNrxnIMMqW6CCeleev2AKcDwyOPSgBFcJxT8ZoZSYzwJhi7q1iUP4pNgUAGSyBI3leRgNtTBImvw07wEiZ-aEtwB-Y1b2IKtIFkoWEb-LOdf9z_kCoKXDHvk14wEfo4WClHogxwfMsVd5jkwTdrTiYdMOQ3rf7Sddns4JKE_4ckmd3qjFahDQONykYfPSDLPQb0OLOxx6IU_2DAqC0BgIRe7QdUPZqvNkgn0alzLmsFpxMq0X6vhPonZnkDc8OLPF6bdcPKCMY8tD-fNK0ZCzy3ngqGR0gwubkq444prYr_jMdZaPK_NDuzT4n8jeAxhIYhQex4mtnVTxVyoytwF5239ABPvxqBE_1EhDEE-wiuxDiV1wlse4eUK0l_6FK_lcW47oOD-XruT1vAG-MJiGveU1hzWU6RESeODo-f_gOBND_hiMlHEh2AbGfWeCzX7EX4dxOv70oo59NzbHs2y4KFq0I=s1024-rj", width=200)

# --- 4. ABAS: CHAT E BUSCA ---
tab1, tab2 = st.tabs(["💬 Chat com o Oráculo", "🔍 Busca de Arquivos"])

with tab1:
    if ia_ativa:
        st.subheader("Pergunte algo ao Oráculo")
        pergunta = st.chat_input("Escreva sua dúvida aqui...")
        if pergunta:
            with st.spinner("O Oráculo está refletindo..."):
                res = model.generate_content(f"Você é o sábio Oráculo. Responda: {pergunta}")
                st.chat_message("assistant").write(res.text)
    else:
        st.warning("O Chat está desativado porque a chave da IA não foi configurada corretamente.")

with tab2:
    st.subheader("Busca no Google Drive")
    # Verificação do Google Drive
    if "google_auth" in st.secrets:
        try:
            creds = service_account.Credentials.from_service_account
