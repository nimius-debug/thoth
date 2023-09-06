import os
from deta import Deta  # pip install deta
from dotenv import load_dotenv  # pip install python-dotenv
import streamlit as st
from typing import Optional



DETA_KEY = st.secrets["DETA_KEY"]
print(DETA_KEY)
# Initialize with a project key
deta = Deta(DETA_KEY)


###############BASE################
# This is how to create/connect a database
db = deta.Base("user_db")

###################Insert################
@st.cache_data
def insert_user(username, name, password):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"key": username, "name": name, "password": password, "school": {},  "events": []})

@st.cache_data
def fetch_all_users():
    """Returns a dict of all users"""
    res = db.fetch()
    return res.items

@st.cache_data
def get_user(username):
    """If not found, the function will return None"""
    return db.get(username)

####################################
###############SCHOOL################
@st.cache_data
def get_user_school(username):
    """If not found, the function will return None"""
    return db.get(username)["school"]

###############EVENTS################
@st.cache_data
def get_user_events(username):
    user_data = db.get(username)
    return user_data.get("events", []) if user_data else []

@st.cache_data
def update_user_events(username, new_events):
    return db.update({"events": new_events}, username)

####################################
@st.cache_data
def update_user(username, updates):
    """If the item is updated, returns None. Otherwise, an exception is raised"""
    return db.update(updates, username)

@st.cache_data
def delete_user(username):
    """Always returns None, even if the key does not exist"""
    return db.delete(username)

###############DRIVE################
# Create/connect to a Deta Drive instance
drive = deta.Drive("knowledge_base")

@st.cache_data
def put_file(username, file_name, file_data):
    try:
        unique_filename = f"{username}_{file_name}"
        drive.put(unique_filename, data=file_data.read())
        return f"Successfully uploaded {file_name}"
    except Exception as e:
        return f"An error occurred while uploading: {e}"

# Fetch a file
@st.cache_data
def get_file(username, file_name):
    try:
        unique_filename = f"{username}_{file_name}"
        return drive.get(unique_filename).read()
    except Exception as e:
        return f"An error occurred while fetching: {e}"

# List all files

def list_files(username):
    try:
        # Fetch the list of all files.
        all_files = drive.list()
        # Extract the 'names' list from the returned dictionary.
        file_names = all_files.get('names', [])
        # Filter and transform the list of file names.
        filtered_files = [name.split(f"{username}_")[1] for name in file_names if name.startswith(username)]
              
        return filtered_files
    except Exception as e:
        return f"An error occurred while listing: {e}"

# Delete a file
@st.cache_data
def delete_file(username, file_name):
    try:
        unique_filename = f"{username}_{file_name}"
        drive.delete(unique_filename)
        return f"Successfully deleted {file_name}"
    except Exception as e:
        return f"An error occurred while deleting: {e}"