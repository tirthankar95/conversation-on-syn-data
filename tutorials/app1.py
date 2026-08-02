import streamlit as st
import numpy as np

with st.chat_message("assistant"):
    st.write("Hello human")
    st.bar_chart(np.random.randn(30, 3))
    name = st.chat_input("What is your name?")
    if name and name.lower() == "tirthankar":
        st.success("Hello Tirthankar! Welcome back!")