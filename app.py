import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Diagnóstico Oráculo")
ak = st.secrets.get("gemini_api")

st.write("# 🔎 Diagnóstico do Oráculo")

if not ak:
    st.error("Chave 'gemini_api' não encontrada nos Secrets!")
else:
    genai.configure(api_key=ak)
    st.success("Chave encontrada! Testando conexão...")
    
    try:
        # Teste direto com o modelo mais comum
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Oi")
        st.write("### ✅ Resposta da IA:")
        st.write(response.text)
    except Exception as e:
        st.write("### ❌ Erro Detalhado:")
        st.code(str(e))
        
        st.write("---")
        st.write("#### Como resolver se o erro for '404' ou 'Method not found':")
        st.write("1. Vá ao [Google AI Studio](https://aistudio.google.com/app/apikey).")
        st.write("2. Verifique se existe um aviso vermelho no topo.")
        st.write("3. Crie uma **NOVA** chave de API.")
        st.write("4. No Streamlit, apague a chave antiga nos Secrets e cole a nova.")
