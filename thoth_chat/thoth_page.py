from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
import database as db

st_callback = StreamlitCallbackHandler(st.container())

from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st

########################################################################




########################################################################
def thoth_page():
    with st.sidebar:
        st.radio("Select a language model", ["Lawyer Thoth", "Math Thoth"])
        st.subheader("knowledge base")
        db_files = db.list_files(st.session_state['username'])
        for file in db_files:
            st.write(file)
            
    llm = OpenAI(temperature=0, streaming=True)
    tools = load_tools(["ddg-search"])
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    if prompt := st.chat_input():
        st.chat_message("user",).write(prompt)
        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(prompt, callbacks=[st_callback])
            st.write(response)