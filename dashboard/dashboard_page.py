
import json
import streamlit as st

from streamlit import session_state as state
from streamlit_elements import elements, sync, event, mui
from types import SimpleNamespace

from dashboard import Dashboard, Editor, Card, DataGrid, Radar, Pie, Player


def dashboard_page(username, name):
    st.title("")
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
    if "w" not in state:
        board = Dashboard()
        w = SimpleNamespace(
            dashboard=board,
            editor=Editor(board, 0, 0, 5, 5, minW=3, minH=3),
            # player=Player(board, 0, 12, 6, 10, minH=5),
            pie=Pie(board, 0, 5, 5, 6, minW=3, minH=4),
            radar=Radar(board, 12, 7, 3, 7, minW=2, minH=4),
            card=Card(board, 6, 7, 3, 7, minW=2, minH=4),
            data_grid=DataGrid(board, 0, 10, 5, 5, minH=4),
        )
        state.w = w

        w.editor.add_tab("Card content", Card.DEFAULT_CONTENT, "plaintext")
        w.editor.add_tab("Data grid", json.dumps(DataGrid.DEFAULT_ROWS, indent=2), "json")
        w.editor.add_tab("Radar chart", json.dumps(Radar.DEFAULT_DATA, indent=2), "json")
        w.editor.add_tab("Pie chart", json.dumps(Pie.DEFAULT_DATA, indent=2), "json")
    else:
        w = state.w

    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

        with w.dashboard(rowHeight=57):
            w.editor()
            # w.player()
            w.pie(w.editor.get_content("Pie chart"))
            w.radar(w.editor.get_content("Radar chart"))
            w.card(w.editor.get_content("Card content"))
            w.data_grid(w.editor.get_content("Data grid"))
