import streamlit as st
import time
from streamlit_gsheets import GSheetsConnection

if 'ws_conn' not in st.session_state:
    st.session_state.ws_conn = st.connection("gsheets", type=GSheetsConnection)

if 'ws_url' not in st.session_state:
    st.session_state.ws_url = "https://docs.google.com/spreadsheets/d/1VFXDHj0NogSQk7jpC0Dw_ML5kQMeM_8WnIxNelrazP8/edit?usp=sharing"

if 'ws_id' not in st.session_state:
    st.session_state.ws_id ={
    'vincent_ws_id':'0',
    'eric_ws_id' : '1073408060',
    'kelvin_ws_id':'2135754122'
    }

url = "https://docs.google.com/spreadsheets/d/1VFXDHj0NogSQk7jpC0Dw_ML5kQMeM_8WnIxNelrazP8/edit?usp=sharing"

option = st.selectbox(
"Runner session",
("VINCENT", "ERIC", "KELVIN"),
index=0,
placeholder ="Select runner here"
)

st.session_state.runner = option
data_placeholder = st.empty()

if st.button('save'):
    st.session_state.ws_conn.update(spreadsheet=st.session_state.ws_url, worksheet= st.session_state.ws_id.get('vincent_ws_id'), data='00:00:00:01')

if st.session_state.runner == 'VINCENT':
    data = st.session_state.ws_conn.read(spreadsheet=st.session_state.ws_url, usecols=[0], worksheet=st.session_state.ws_id.get('vincent_ws_id'))
    data_placeholder.dataframe(data)
elif st.session_state.runner =='ERIC':
    data = st.session_state.ws_conn.read(spreadsheet=st.session_state.ws_url, usecols=[0], worksheet=st.session_state.ws_id.get('eric_ws_id'))
    data_placeholder.dataframe(data)
elif st.session_state.runner =='KELVIN':
    data = st.session_state.ws_conn.read(spreadsheet=st.session_state.ws_url, usecols=[0], worksheet=st.session_state.ws_id.get('kelvin_ws_id'))
    data_placeholder.dataframe(data)


