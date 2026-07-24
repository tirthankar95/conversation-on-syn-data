import streamlit as st

# Configure page to wide layout
st.set_page_config(layout="wide")

# Custom CSS for dark button accents
st.markdown(
    """
    <style>
    /* Force Primary Buttons to be solid Black with White Text */
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

    /* Force Secondary Buttons to be Light Gray with Black Text */
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

# -----------------------------------------------------------------------------
# 1. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("Chat Data Faker")
    
    # Clicking the text name acts as a button
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Data Generation"
        
    if st.button("Data Generation", use_container_width=True, key="nav_data_gen"):
        st.session_state.active_page = "Data Generation"

    if st.button("Talk to your data", use_container_width=True, key="nav_talk_data"):
        st.session_state.active_page = "Talk to your data"
    
    st.divider()
    
    # Sidebar controls specific to active page mode
    if st.session_state.active_page != "Data Generation":
        st.write("### Chat Settings")
        st.selectbox("Model", ["GPT-4o", "Claude 3.5 Sonnet", "Llama 3"])
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

# -----------------------------------------------------------------------------
# 2. MAIN PAGE SWITCHING
# -----------------------------------------------------------------------------

if st.session_state.active_page == "Data Generation":
    # --- DATA GENERATION VIEW ---
    # Row 1: Top Element
    top_row = st.container(border=True)
    with top_row:
        st.text_input(
            "Prompt",
            placeholder="Enter your prompt here...",
            help="Enter additional instructions which would go with the DDL schema to generate synthetic data."
        )
        st.button(
            "Upload DDL Schema",
            icon=":material/upload_file:",
            type="primary",
        )
        
        col1, col2 = st.columns(2)
        with col1:
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
        with col2:
            st.text_input(
                "Max Tokens",
                placeholder="100"
            )
        st.button(
            "Generate",
            type="primary",
            icon=":material/auto_awesome:",
        )

    # Row 2: Bottom Element
    bottom_row = st.container(border=True)
    with bottom_row:
        header, select_col = st.columns(2)
        
        available_files = [
            "Select a file...",
            "company_employee_schema.ddl",
            "library_mgm_schema.ddl",
            "restaurants_schema.ddl",
        ]
        
        with header:
            st.write("#### Data Preview")
            
        with select_col:
            selected_file = st.selectbox(
                "",
                options=available_files,
                index=0,
                help="Choose a schema to inspect its generated contents.",
            )
            
        st.divider()

        if selected_file and selected_file != "Select a file...":
            st.info(f"Displaying content preview for **{selected_file}**...")
            
            st.code(
                f"""-- Sample Schema preview for {selected_file}
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'active'
);""",
                language="sql",
            )
        else:
            st.text("No file selected.")


elif st.session_state.active_page == "Talk to your data":
    # --- TALK TO YOUR DATA VIEW ---
    st.header("Talk to Your Data")
    st.caption("Ask questions about your uploaded schemas and generated data.")
    
    chat_container = st.container(border=True)
    with chat_container:
        st.chat_message("assistant").write("Hello! Ask me anything about your generated synthetic dataset.")
        
    st.chat_input("Ask a query about your tables...")