import streamlit as st
import streamlit_authenticator as stauth
import database as db
from streamlit_option_menu import option_menu
from PIL import Image




st.set_page_config(page_title="Thoth", page_icon="📚",layout="wide")
# from dashboard.dashboard_page import dashboard_page
from min_dashboard.dashboard import display_dashboard
from book_notes.book_note_page import book_note_page
from thoth_chat.thoth_page import thoth_page
from settings.settings_page import setting_p
######### Configuration #####################
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/


def initialize_session_state():
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None

initialize_session_state()



# Configuration for static values
MENU_OPTIONS = ["Dashboard", "Talk to Thoth", "Books/Notes", 'Settings']
MENU_ICONS = ['speedometer2', 'chat-dots', "journal-arrow-up", 'gear']
MENU_STYLES = {
    "container": {
        "padding": "10px!important", 
        "background-color": "#0F1D2B",  
        "border": "2px solid #26A69A" 
    },
    "icon": {
        "color": "#B2EBF2",  
        "font-size": "16px", 
        "margin-right": "5px"
    },
    "nav-link": {
        "font-size": "16px", 
        "text-align": "left", 
        "margin":"5px 0", 
        "padding": "5px 10px",
        "--hover-color": "#1A3547"  
    },
    "nav-link-selected": {
        "background-color": "#26A69A",  
        "color": "#E8F1F2",  
        "border-left": "4px solid #B2EBF2"  
    }
}

###########################################################

def create_login_widget(credentials):
    authenticator = stauth.Authenticate(
        credentials, 
        "thoth_dashboard", 
        st.secrets["SECRET_KEY"],
        cookie_expiry_days=1
    )
    name, authentication_status, username = authenticator.login("Login", "main")
    return name, authentication_status, username, authenticator

@st.cache_data
def user_credentials(users):
    
    credentials = {"usernames": {}}

    for user in users:
        username = user["key"]
        name = user["name"]
        hashed_password = user["password"]
        
        user_dict = {
            "name": name,
            "password": hashed_password
        }
        
        credentials["usernames"][username] = user_dict

    return credentials

def get_session_value(key, default=None):
    return st.session_state.get(key, default)

def display_sidebar():
    with st.sidebar:
        img_logo = Image.open("img/thoth_s.webp")
        st.image(img_logo,width=60 )
        return option_menu(None, MENU_OPTIONS, icons=MENU_ICONS, menu_icon="cast", default_index=0, styles=MENU_STYLES)

def main():
        
    try:
        users = db.fetch_all_users()
        credentials = user_credentials(users)
        
        # Step 3: Creating a Login Widget
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            placeholder = st.empty()
            img = Image.open("img/thoth_white1.webp")
            # Replace the chart with several elements:
            with placeholder.container():
                st.info("Demo credentials|  username: pparker, password: def456")
                st.info("Demo credentials|  username: rmiller, password: def456")
                st.markdown("---")
                col11, col22, col33 = st.columns([1, 1, 1])
                with col22:
                    st.image(img,use_column_width=True )
            
            # placeholder.title("Thoth")
            name, authentication_status, username, authenticator = create_login_widget(credentials)
            st.session_state['authentication_status'] = authentication_status
        
        auth_status = get_session_value('authentication_status')
        
        if auth_status == False:
            col2.error("Username/password is incorrect")
        elif auth_status == None:
            col2.warning("Please enter your username and password")
        else: 
            placeholder.empty()
            selected_option = display_sidebar()
            authenticator.logout("Logout", "sidebar")

            if selected_option == "Dashboard":
                display_dashboard( name,username)
            elif selected_option == "Talk to Thoth":
                thoth_page()
            elif selected_option == "Books/Notes":
                book_note_page(username)
            elif selected_option == "Settings":
                setting_p(username, name)
                
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()