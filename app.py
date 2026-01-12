import streamlit as st
import os

# Define o nome da pasta que você criou no GitHub
PASTA_DOCS = "documentos"

st.title("🔮 Oráculo")

busca = st.text_input("Digite o problema:")

if busca:
    # O comando abaixo lista TUDO que está dentro da pasta 'documentos'
    if os.path.exists(PASTA_DOCS):
        arquivos = os.listdir(PASTA_DOCS)
        
        # Filtra os arquivos que contêm a palavra que o usuário digitou
        resultados = [f for f in arquivos if busca.lower() in f.lower()]
        
        if resultados:
            for nome_arquivo in resultados:
                caminho_completo = os.path.join(PASTA_DOCS, nome_arquivo)
                
                # Abre o arquivo e cria o botão de baixar no app
                with open(caminho_completo, "rb") as f:
                    st.download_button(
                        label=f"📄 Baixar {nome_arquivo}",
                        data=f,
                        file_name=nome_arquivo
                    )
        else:
            st.warning("Nenhum documento encontrado.")
    else:
        st.error("A pasta 'documentos' não foi encontrada no GitHub.")
