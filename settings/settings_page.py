import streamlit as st
import database as db

def setting_p(username, name):
    
    with st.form(key="user_form"):
        col1, col2 = st.columns([6, 1], gap="large")
        with col1:
            st.header(f"User Info {username}")

            user_school_data = db.get_user_school(username)
           
            student_name = st.text_input(label="Student Name", value=name)
        
            school_name = st.text_input(label="School Name", value=user_school_data.get("school_name", " "))
            
            roll_number = st.text_input(label="Roll Number", value=user_school_data.get("roll_number", " "))
            
            school_dep = st.text_input(label="Department", value=user_school_data.get("department", " "))
            
            school_year = st.text_input(label="Year", value=user_school_data.get("year", " "))
            
        with col2:
            st.image(f"https://robohash.org/{name}.png",use_column_width=True )
        
        saved_click = st.form_submit_button(label="Save")
        if saved_click:
            user_school_data = {
                "school_name": school_name,
                "roll_number": roll_number,
                "department": school_dep,
                "year": school_year,
            }
            db.update_user(username, user_school_data)
            st.toast("Saved Successfully!")
     
        