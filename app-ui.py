import streamlit as st


def _init_state() -> None:
    if "uploaded_ddls" not in st.session_state:
        st.session_state.uploaded_ddls = {}


def _save_uploaded_file(uploaded_file) -> None:
    if uploaded_file is None:
        return
    st.session_state.uploaded_ddls[uploaded_file.name] = uploaded_file.getvalue().decode(
        "utf-8", errors="replace"
    )


def _render_uploaded_files() -> None:
    st.subheader("Uploaded .ddl Files")
    files = st.session_state.uploaded_ddls

    if not files:
        st.info("No .ddl files uploaded yet.")
        return

    for name, content in files.items():
        with st.expander(name):
            st.code(content, language="sql")


def main() -> None:
    st.set_page_config(page_title="DDL Upload UI", layout="wide")
    _init_state()

    st.title("Synthetic Data Assistant")
    st.write("Use the right-side tabs to upload one or many .ddl schema files.")

    left_col, right_col = st.columns([1.5, 1])

    with right_col:
        _render_uploaded_files()

    with left_col:
        st.subheader("Upload Panel")
        upload_tab, multi_tab = st.tabs(["Single Upload", "Bulk Upload"])

        with upload_tab:
            file = st.file_uploader(
                "Upload one schema file",
                type=["ddl"],
                accept_multiple_files=False,
                key="single_ddl",
            )
            if file is not None:
                _save_uploaded_file(file)
                st.success(f"Uploaded: {file.name}")

        with multi_tab:
            files = st.file_uploader(
                "Upload multiple schema files",
                type=["ddl"],
                accept_multiple_files=True,
                key="multi_ddl",
            )
            if files:
                for uploaded in files:
                    _save_uploaded_file(uploaded)
                st.success(f"Uploaded {len(files)} file(s).")

        if st.session_state.uploaded_ddls:
            if st.button("Clear uploaded files", use_container_width=True):
                st.session_state.uploaded_ddls = {}
                st.rerun()


if __name__ == "__main__":
    main()
