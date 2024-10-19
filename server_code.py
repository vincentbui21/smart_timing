import time
import streamlit as st

st.info('hi')
with st.spinner('wait'):
    time.sleep(5)
st.success('Done')