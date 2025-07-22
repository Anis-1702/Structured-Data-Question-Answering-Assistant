# StreamlitApp.py

import streamlit as st
from langgraph_duckdb import ask_question  # <- updated import

st.set_page_config(page_title="Structured Data Assistant", layout="wide")
st.title("📊 Structured Data Q&A Assistant")

user_query = st.text_input("Enter your question about the data:", "")

if st.button("Ask") and user_query:
    with st.spinner("Thinking..."):
        answer = ask_question(user_query)
    st.markdown("### 📥 Answer:")
    st.markdown(f"```\n{answer}\n```")
