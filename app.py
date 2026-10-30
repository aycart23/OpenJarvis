import sys
import subprocess

# Instalación automática blindada para Streamlit Cloud
try:
    import groq
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "groq==0.4.2"])
    import groq

import streamlit as st
from groq import Groq

st.set_page_config(page_title="JARVIS - Sistema Central", page_icon="⚡")

st.title("⚡ J.A.R.V.I.S. Cloud")
st.caption("Sistema de Asistencia Autónoma - En línea 24/7")

# Obtener la llave de la IA desde los Secrets de Streamlit
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ Señor, falta configurar la llave GROQ_API_KEY en las opciones avanzadas.")
else:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Eres JARVIS, el asistente de inteligencia artificial de Tony Stark. Respondes con elegancia, precisión, un toque de ironía británica y absoluta eficiencia profesional."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Escriba su orden, jefe..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
