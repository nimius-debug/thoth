import streamlit as st
import database as db
import pandas as pd
from streamlit_calendar import calendar
from datetime import date ,datetime, timedelta
import uuid
from streamlit_extras.colored_header import colored_header

@st.cache_data
def style_metric_cards(
    background_color: str = "#1A3547", # Matching secondaryBackgroundColor
    border_size_px: int = 1,
    border_color: str = "#26A69A",  # Matching primaryColor
    border_radius_px: int = 5,
    border_left_color: str = "#26A69A",  # Matching primaryColor
    box_shadow: bool = True,
    text_color: str = "#B2EBF2"  # Matching textColor
):
    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )

    st.markdown(
        f"""
        <style>
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                color: {text_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                {box_shadow_str}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def display_dashboard(name, username):
    
    with st.form(key="user_form"):
        col1, col2 = st.columns([6, 1], gap="large")
        with col1:
            st.header(f"Welcome {username}")
            col11, col22, col33, col44, col55 = st.columns([1, 1, 1, 1, 1])
            user_school_data = db.get_user_school(username)
            with col11:
                st.text_input(label="Student Name", value=name,disabled=True)
            with col22:
                school_name = st.text_input(label="School Name", value=user_school_data.get("school_name", " "))
            with col33:
                roll_number = st.text_input(label="Roll Number", value=user_school_data.get("roll_number", " "))
            with col44:
                school_dep = st.text_input(label="Department", value=user_school_data.get("department", " "))
            with col55:
                school_year = st.text_input(label="Year", value=user_school_data.get("year", " "))
            
        with col2:
            st.image(f"https://robohash.org/{name}.png",use_column_width=True )
        
        saved_click = st.form_submit_button(label="Save")
        if saved_click:
            user_school_data = {
                "school": {
                    "school_name": school_name,
                    "roll_number": roll_number,
                    "department": school_dep,
                    "year": school_year,
                }
            }
            db.update_user(username, user_school_data)
            st.toast("Saved Successfully!")
    
   ##############################################################################
    colored_header(
        label="Classes",
        description="Add and update your classes",
        color_name="blue-green-70",
    )
    #########################Metrics-Classses#########################
    @st.cache_data
    def transform_dataframe(df):
        if df is not None and 'exams' in df.columns:
            if 'exam_1' not in df.columns:
                exams_df = pd.DataFrame(df['exams'].to_list(), columns=['exam_1', 'exam_2', 'exam_3'])
                df = pd.concat([df, exams_df], axis=1)
        return df
    
    @st.cache_data
    def update_exams_column(df):
        df['exams'] = df[['exam_1', 'exam_2', 'exam_3']].values.tolist()
        return df
    
    # Initialize session state
    if "classes_data" not in st.session_state:
        # Attempt to retrieve the class data from the database
        cls_data = db.get_user_class(username)
        
        # If data exists in database, use it; otherwise, create an empty DataFrame
        if cls_data is not None:
            df = pd.DataFrame.from_dict(cls_data)
            st.session_state.classes_data = transform_dataframe(df)
        else:
            st.session_state.classes_data = pd.DataFrame(
                 columns=["subject", "teacher", "grade", "exam_1", "exam_2", "exam_3", "exams"]
            )
            
    with st.form(key='save_classes'):
        edited_df = st.data_editor(
                st.session_state.classes_data,
                key="editor",
                num_rows="dynamic",
                column_order=("subject", "teacher", "grade", "exam_1", "exam_2", "exam_3", "exams"),
                use_container_width=True,
                column_config={
                "exams": st.column_config.LineChartColumn(
                        "Progress",
                        width="medium",
                        y_min=50,
                        y_max=100,
                    ),
                "exam_1": st.column_config.NumberColumn(
                        "Exam 1",
                        width="small",
                        default=80,
                        min_value=0,
                        max_value=150,
                    ),
                "exam_2": st.column_config.NumberColumn(
                        "Exam 2",
                        width="small",
                        default=82,
                        min_value=0,
                        max_value=150,
                    ),
                "exam_3": st.column_config.NumberColumn(
                        "Exam 3",
                        width="small",
                        default=81,
                        min_value=0,
                        max_value=150,
                    ),
                "teacher": st.column_config.TextColumn(
                        "Teacher",
                        width="medium",
                        default="Mr. Doe",
                        # required=True,
                    ),
                "grade": st.column_config.TextColumn(
                        "Grade",
                        width="small",
                        default="B",
                        # required=True,
                    ),
                },      
            )
        
        save_button = st.form_submit_button(label='Save')
        if save_button:
            if edited_df is not None and not edited_df.equals(st.session_state.classes_data):
                with st.status("Updating classes..."):
                    edited_df = update_exams_column(edited_df)  # Update 'exams' based on individual exams
                    st.session_state.classes_data = edited_df  # Update the session state
                    db.update_user_class(username, edited_df.to_dict('records'))
                    st.rerun()  # Rerun the app to reflect the changes
            
    # Display the classes metrics
     ##############################Metrics###############################
    st.markdown("  \n")
    # classes_metrics_container = st.container()
    if st.session_state.classes_data is not None and not st.session_state.classes_data.empty:
        num_classes = len(st.session_state.classes_data)
        print(f"Num classes before columns: {num_classes}")  # Debug print

        # Create columns dynamically based on the number of classes
        columns = st.columns(num_classes + 1)

        # The first column shows the total number of classes
        with columns[0]:
            st.metric(label="Total Classes", value=num_classes)
            
        # Each subsequent column shows a metric for each class
        for i, (index, row_data) in enumerate(st.session_state.classes_data.iterrows()):
            with columns[i + 1]:
                label = row_data['subject']
                value = row_data['grade']
                delta = row_data['exam_3'] - ((row_data['exam_1'] + row_data['exam_2']) / 2)
                print(delta)
                st.metric(label=label, value=value, delta=delta)
                
                # Your code for displaying class data here
    else:
        st.write("No class data available or class data is empty.")
    style_metric_cards()
    # Number of classes the user has
    
    ##############################Classes###############################    
            
             
        
    ##############################CALENDAR################################
    st.markdown("  \n")
    st.markdown("  \n")
    
    if 'events' not in st.session_state:
        st.session_state.events = db.get_user_events(username)
    # Initialize session state for events
    colored_header(
        label="Calendar & Assignments ",
        description="Add your assignments & classes ",
        color_name="light-blue-70",
    )
   # UI for adding new event
    col1, col2 = st.columns([1, 1])
    with col1:
        recurrence_type = st.selectbox("Recurrence Type", ['None', 'Daily', 'Weekly'])
        if recurrence_type == 'None':
            with st.form("new_event_form"):
                event_name = st.text_input("Event Name")
                event_date = st.date_input("Event Date")
                event_start_time = st.time_input("Start Time")
                event_end_time = st.time_input("End Time")
                color = st.color_picker("Pick a color for the event", "#00f900")
                
                add_event_button = st.form_submit_button("Add Event")
                # Add event to session state
                if add_event_button:
                    start_datetime = datetime.combine(event_date, event_start_time).isoformat()
                    end_datetime = datetime.combine(event_date, event_end_time).isoformat()
                    new_event = {
                        'id': str(uuid.uuid4()),  # Generate a random UUID
                        "title": event_name,
                        "start": start_datetime,
                        "end": end_datetime,
                        "color": color,
                    }
                    st.session_state.events.append(new_event)
                    db.update_user_events(username, st.session_state.events)
        else:
            with st.form("recurring_event"):
                event_name = st.text_input("Event Name")
                event_start_time = st.time_input("Start Time")
                event_end_time = st.time_input("End Time")
                start_date = st.date_input("Start Date" )
                end_date = st.date_input("End Date")
                color = st.color_picker("Pick a color for the event", "#00f900")
               
                add_recurring_event = st.form_submit_button("Add Recurring Event")

                if add_recurring_event:
                  
                    if start_date > end_date:
                        st.error("Start date cannot be after end date")
                        st.stop()
                    
                    while start_date <= end_date:
                        new_event = {
                            'id': str(uuid.uuid4()),  # Generate a random UUID
                            'title': event_name,
                            'start': datetime.combine(start_date, event_start_time).isoformat(),
                            'end': datetime.combine(start_date, event_end_time).isoformat(),
                            'color': color
                        }
                        st.session_state.events.append(new_event)

                        if recurrence_type == 'Daily':
                            start_date += timedelta(days=1)
                        elif recurrence_type == 'Weekly':
                            start_date += timedelta(weeks=1)
                            
                    db.update_user_events(username, st.session_state.events)
    with col2:
        # Calendar mode selector
        today = date.today().isoformat()

        # Base calendar options
        calendar_options = {
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridDay,dayGridWeek,dayGridMonth",
            },
            "editable": "false",
            "navLinks": "false",
            "slotMinTime": "06:00:00",
            "slotMaxTime": "18:00:00",
            "initialDate": today,  # Set it to today
            "initialView": "dayGridMonth",
        }


        # Display the calendar with the selected mode and events
        state = calendar(events=st.session_state.events, options=calendar_options)
        # Capture clicked event data from calendar state
        clicked_event = state.get('eventClick')
        if clicked_event:
            event_id = clicked_event['event']['id']  # Assumes each event has a unique 'id' field
            print(event_id)
            if st.button(f"Delete event {event_id}?"):
                # Remove event from session state
                st.session_state.events = [event for event in st.session_state.events if event['id'] != event_id]
                
                # Update events in the database
                db.update_user_events(username, st.session_state.events)
                
                # Show a confirmation message
                st.toast(f"Deleted event {event_id}")
                st.rerun()
                
        if st.button("Clear All Events"):
            st.session_state.events = []
            db.update_user_events(username, [])
            st.rerun()
            
    ##############################CALENDAR################################