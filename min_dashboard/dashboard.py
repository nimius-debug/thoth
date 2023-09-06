import streamlit as st
import database as db
from streamlit_calendar import calendar
from datetime import date ,datetime, timedelta


def display_dashboard(name, username):

    user_school_data = db.get_user_school(username)
  
    with st.form(key="user_form"):
        col1, col2 = st.columns([6, 1], gap="large")
        with col1:
            st.header(f"Welcome {username}")
            col11, col22, col33, col44, col55 = st.columns([1, 1, 1, 1, 1])
            with col11:
                st.text_input(label="Student Name", value=name)
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
                "school_name": school_name,
                "roll_number": roll_number,
                "department": school_dep,
                "year": school_year,
            }
            db.update_user(username, user_school_data)
            st.toast("Saved Successfully!")
    
    ##############################CALENDAR################################
    if 'events' not in st.session_state:
        st.session_state.events = []
    # Initialize session state for events
 

   # UI for adding new event
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Add New Event")
        recurrence_type = st.selectbox("Recurrence Type", ['None', 'Daily', 'Weekly'])
        if recurrence_type == 'None':
            with st.form("new_event_form"):
                event_name = st.text_input("Event Name")
                event_date = st.date_input("Event Date")
                event_start_time = st.time_input("Start Time")
                event_end_time = st.time_input("End Time")
                add_event_button = st.form_submit_button("Add Event")

                # Add event to session state
                if add_event_button:
                    start_datetime = datetime.combine(event_date, event_start_time).isoformat()
                    end_datetime = datetime.combine(event_date, event_end_time).isoformat()

               
                    new_event = {
                        "title": event_name,
                        "start": start_datetime,
                        "end": end_datetime
                    }
                    st.session_state.events.append(new_event)
                
        else:
            with st.form("recurring_event"):
                event_name = st.text_input("Event Name")
                event_start_time = st.time_input("Start Time")
                event_end_time = st.time_input("End Time")
                start_date = st.date_input("Start Date", min_value=date.today())
                end_date = st.date_input("End Date", min_value=start_date)
               
                add_recurring_event = st.form_submit_button("Add Recurring Event")

                if add_recurring_event:
                    current_date = start_date
                    while current_date <= end_date:
                        new_event = {
                            'title': event_name,
                            'start': datetime.combine(current_date, event_start_time).isoformat(),
                            'end': datetime.combine(current_date, event_end_time).isoformat(),
                        }
                        st.session_state.events.append(new_event)

                        if recurrence_type == 'Daily':
                            current_date += timedelta(days=1)
                        elif recurrence_type == 'Weekly':
                            current_date += timedelta(weeks=1)
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