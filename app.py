import streamlit as st

st.title("Meu Primeiro App Web")
st.header("Seja bem-vindo!")
st.write("Este site foi criado usando apenas Python e Streamlit.")

nome = st.text_input("Digite seu nome:")
if nome:
    st.write(f"Olá {nome}, seu app está funcionando!")
col1, col2 = st.columns(2)

with col1:
    st.header("Coluna 1")
    st.button("Botão na esquerda")

with col2:
    st.header("Coluna 2")
    st.write("Texto na direita")
