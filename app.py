import streamlit as st
import os
import base64

st.set_page_config(page_title="Oráculo", page_icon="🔮")

st.title("🔮 Oráculo de Documentos")

PASTA_DOCS = "documentos"

# Função para ler o arquivo e criar um link de visualização
def gerar_link_visualizacao(caminho_arquivo, nome_arquivo):
    with open(caminho_arquivo, "rb") as f:
        dados = f.read()
    
    # Converte o arquivo para base64
    base64_pdf = base64.b64encode(dados).decode('utf-8')
    
    # Determina o tipo de arquivo (PDF ou Texto/Imagem)
    if nome_arquivo.lower().endswith('.pdf'):
        tipo = "application/pdf"
    else:
        tipo = "application/octet-stream"

    # Cria um link HTML que abre o arquivo em uma nova aba
    href = f'<a href="data:{tipo};base64,{base64_pdf}" target="_blank" style="text-decoration: none;">' \
           f'<div style="background-color: #4CAF50; color: white; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px;">' \
           f'📄 Abrir: {nome_arquivo}</div></a>'
    return href

busca = st.text_input("O que você deseja encontrar?", placeholder="Ex: lentidão...")

if busca:
    if os.path.exists(PASTA_DOCS):
        arquivos = os.listdir(PASTA_DOCS)
        resultados = [f for f in arquivos if busca.lower() in f.lower()]
        
        if resultados:
            st.write(f"### ✅ Resultados encontrados:")
            for nome_arquivo in resultados:
                caminho_completo = os.path.join(PASTA_DOCS, nome_arquivo)
                
                # Gera o botão/link que abre o arquivo
                link_html = gerar_link_visualizacao(caminho_completo, nome_arquivo)
                st.markdown(link_html, unsafe_allow_html=True)
        else:
            st.warning("Nenhum documento encontrado.")
    else:
        st.error("Pasta 'documentos' não encontrada.")
