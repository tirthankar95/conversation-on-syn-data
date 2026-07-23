import streamlit as st

# Configure page to wide layout so side-by-side elements have room to breathe
st.set_page_config(layout="wide")

# -----------------------------------------------------------------------------
# 1. NARROW LEFT PANEL (Sidebar with Text Label Tabs)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("Chat DataFaker")
    
    # Text-label tabs inside the sidebar
    tab_a, tab_b = st.tabs(["Data Generation", "Talk to your data"])
    
    with tab_a:
        st.write("### Overview Controls")
        st.text_input("Project Name", value="My Analysis")
        st.selectbox("Filter Status", ["All", "Active", "Archived"])
        
    with tab_b:
        st.write("### Preferences")
        st.checkbox("Enable Dark Mode", value=True)
        st.slider("Refresh Rate (s)", 1, 60, 5)

# -----------------------------------------------------------------------------
# 2. MAIN PAGE (Divided into Two Elements)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Force Primary Buttons (Generate) to be solid Black with White Text */
    button[kind="primary"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #000000 !important;
    }
    button[kind="primary"]:hover {
        background-color: #222222 !important;
        color: #ffffff !important;
        border-color: #222222 !important;
    }
    button[kind="primary"] * {
        color: #ffffff !important;
    }

    /* Force Secondary Buttons (Upload) to be Light Gray with Black Text */
    button[kind="secondary"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
    }
    button[kind="secondary"]:hover {
        background-color: #f0f0f0 !important;
        color: #000000 !important;
        border-color: #000000 !important;
    }
    button[kind="secondary"] * {
        color: #000000 !important;
    }

    /* Change slider color to black */
    div[data-baseweb="slider"] div {
        background-color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Row 1: Top Element
top_row = st.container(border=True)
with top_row:
    st.text_input(
                "Prompt",
                placeholder="Enter your prompt here...",
                help="Enter additional instructions which would go with the DDL schema to generate synthetic data."
            )
    st.button("Upload DDL Schema",
            icon=":material/upload_file:",  # Native Streamlit upload icon
            type="primary",)
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    with col2:
        st.text_input(
                "Max Tokens",
                placeholder = 100
            )
    st.button(
            "Generate",
            type="primary",
            icon=":material/auto_awesome:",
        )

# Row 2: Bottom Element
bottom_row = st.container(border=True)
with bottom_row:
    st.write("### Generated Data")