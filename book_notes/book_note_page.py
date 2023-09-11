import streamlit as st
import database as db

def book_note_page():
    st.title("Books/Notes")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Upload Your Documents to Thoth")
        st.write("Enhance Thoth's capabilities and personalize your academic assistance by uploading your study materials. \
            Each document you add contributes to your unique knowledge base, enabling Thoth AI to provide more targeted and \
            accurate academic support. Simply click the \"Upload Documents\" button to start empowering your learning experience.")
    with col2:
        uploaded_file = st.file_uploader("Upload Documents", type=["pdf"])
        if uploaded_file is not None:
            result_message = db.put_file(st.session_state['username'], uploaded_file.name, uploaded_file)
            st.toast(result_message)
    
    st.divider()
    st.subheader("Your Documents")

    try:
        with st.status("Loading your documents..."):
            db_files = db.list_files(st.session_state['username'])
        
        if not isinstance(db_files, list) or len(db_files) == 0:
            st.write("You have not uploaded any documents yet.")
        else:
            files_to_delete = []
            with st.form("file_deletion_form", clear_on_submit=True):
                for file in db_files:
                    checked = st.checkbox(f"{file}")
                    if checked:
                        files_to_delete.append(file)
                
                delete_button = st.form_submit_button("Delete Selected Files")
                if delete_button:
                    for file in files_to_delete:
                        result_message = db.delete_file(st.session_state['username'], file)
                        st.toast(result_message)
                    st.experimental_rerun()
    except Exception as e:
        st.write(f"An error occurred: {e}")
            