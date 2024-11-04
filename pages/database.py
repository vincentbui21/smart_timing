import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from natsort import index_natsorted

st.set_page_config(
    page_title="Data Base",
    page_icon="📊",
)

conn = st.connection("gsheets", type=GSheetsConnection)

def update_new_timestamp(timestamp:str, runner:str) -> None:
    existing_data = conn.read(worksheet=runner, ttl=5)
    runner_data = pd.DataFrame(
        [
            {
                "TIMESTAMP HISTORY": timestamp
            }
        ]
    )
    new_data = pd.concat([existing_data, runner_data], ignore_index=True)
    conn.update(worksheet=runner, data = new_data)


if __name__ == "__main__":
    option = st.selectbox(
    "Choose runner's name to see/update data",
    ('VINCENT', 'ERIC', 'KELVIN'),
)

    data = conn.read(worksheet=option, ttl=5)
    
    st.dataframe(data)
    chart_data = pd.DataFrame(data)
    
    chart_data.sort_values(by='TIMESTAMP HISTORY', ascending=True)

    st.area_chart(chart_data, y='TIMESTAMP HISTORY')

    data= st.text_input('New timestamp')
    if st.button('Save data'):
        update_new_timestamp(timestamp=data, runner=option)
        st.toast('Done!')