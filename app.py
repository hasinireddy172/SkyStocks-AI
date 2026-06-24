
import streamlit as st
from agent import run_agent


st.set_page_config(
    page_title="Multi Tool AI",
    page_icon="🤖"
)

st.title("🤖 Multi Tool AI")

prompt = st.text_input(
    "Enter your prompt"
)

if st.button("Submit"):

    if prompt:

        with st.spinner("Thinking..."):
            result = run_agent(prompt)

        st.write(result)