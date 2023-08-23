import streamlit as st
import database as db
import pandas as pd
import numpy as np
from streamlit_elements import elements, mui, html, editor, nivo, sync, lazy, dashboard, event


def display_dashboard(name, username):
    col1, col2 = st.columns([6, 1],gap="large")
    with col1 :
        st.header(f"Welcome {username}")
        with elements("student_details"):
            mui.TextField(label="Student Name", value=name,shrink=True,width="auto")
            mui.TextField(label="School Name", value="MIT")
            mui.TextField(label="Roll Number",value="123456789")
            mui.TextField(label="Department")
            mui.TextField(label="Year")
        # st.subheader("MIT, 3th Year")
    with col2:
        st.image(f"https://robohash.org/{name}.png",use_column_width=True )
    
    st.divider()
    st.markdown('#') 
    # fetch from database to create data
    user_data = db.get_user(username)
    print(user_data)
    
    
    col1, col2, col3 = st.columns(3)
    col1.metric("MATH", "94", "1.2 ")
    col2.metric("ENGINEERING", "86", "-5.1")
    col3.metric("LAW", "86", "4.0")
    st.markdown('#') 
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.line_chart(chart_data)
    
    with elements("dashboard"):
    # Sample layout
        layout = [
            dashboard.Item("task_component", 0, 0, 2, 2)
        ]
        # Handle layout changes
        def handle_layout_change(updated_layout):
            print(updated_layout)
        
        def handle_clik_task():
            print("clicked")
        st.title("My Draggable Dashboard")
    
        # Store tasks using session state
        if "tasks" not in st.session_state:
            st.session_state.tasks = []

        # Create a dashboard layout
   
        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            with mui.Paper("TASK", key="task_component"):
              
            # mui.Checkbox(task, key=f"checkbox_{index}")
            # mui.Typography(task)

                # Using Material UI Textfield (mui.TextField) for input
                mui.TextField("Add a new task:", key="new_task_input")
               
                mui.Button("Add", onClick=handle_clik_task)
                    # st.session_state.tasks.append(new_task)
