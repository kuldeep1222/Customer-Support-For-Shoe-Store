import streamlit as st
from Agents import run_agent

st.set_page_config(
    page_title="Customer Support For Shoe Store",
    page_icon="👟",
    layout="wide"
)

st.title("👟 Customer Support For Shoe Store")

st.write("Ask about products, orders, recommendations, or comparisons.")

question = st.text_input("Enter your question")

if st.button("Ask"):

    if question.strip():

        with st.spinner("Thinking..."):

            answer = run_agent(question)

        st.markdown(answer)

    else:

        st.warning("Please enter a question.")