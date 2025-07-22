import streamlit as st
from langgraph_app import ask_question

st.set_page_config(page_title="📊 Structured Data Assistant", layout="centered")
st.title("📊 Structured Data Assistant")

user_query = st.text_input("Ask a data question:", placeholder="e.g. What was the churn in AAA last month?")

if user_query:
    with st.spinner("Thinking..."):
        result = ask_question(user_query)
    st.success("Answer:")
    st.write(result)