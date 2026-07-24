import streamlit as st
from app3_frontend.chat import apply_chat
from app3_frontend.side_nav import apply_side_bar
from app3_frontend.data_gen import apply_data_gen
from app3_frontend.style import apply_custom_styles

# Configure page to wide layout
st.set_page_config(layout="wide")

apply_custom_styles(st)

# -----------------------------------------------------------------------------
# 1. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
apply_side_bar(st)

# -----------------------------------------------------------------------------
# 2. MAIN PAGE SWITCHING
# -----------------------------------------------------------------------------
if st.session_state.active_page == "Data Generation":
    apply_data_gen(st)
if st.session_state.active_page == "Talk to your data":
    apply_chat(st)