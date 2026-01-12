import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
st.set_page_config(page_title="Oráculo", layout="wide")

# Perseguição em ângulos variados (100% CSS)
st.markdown("""
<style>
@keyframes rato {
  0% { top: 10%; left: 10%; }
  25% { top: 80%; left: 30%; }
  50% { top: 20%; left: 80%; }
  75% { top: 70%; left: 60%; }
  100% { top: 10%; left: 10%; }
}
@keyframes gato {
  0% { top: 15%; left: 5%; }
  25% { top: 85%; left: 25%; }
  50% { top: 25%; left: 75%; }
  75% { top: 75%; left: 55%; }
  100% { top: 15%; left: 5%; }
}
.rat { position: fixed; font-size: 30px; animation: rato 8s linear infinite; z-index: 99; }
.cat { position: fixed; font-size: 45px; animation: gato 8s linear infinite; z-index: 100; }
@keyframes f { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-15px) } }
.b { font-size: 70px; text-align: center; animation: f 3s infinite; }
</style>
<div class="rat">🐭</div>
<div class="cat">
