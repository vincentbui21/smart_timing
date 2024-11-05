import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from natsort import index_natsorted

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
    st.divider()
    place_holder = st.empty()
    col1, col2 = place_holder.columns(2)

    data = conn.read(worksheet=option, usecols=[0, 1],ttl=5)
    col1.dataframe(data, width=300, height=500)
    
    col2.text_input('New timestamp')
    if col2.button('Save data'):
        update_new_timestamp(timestamp=data, runner=option)
        st.toast('Done!')

    st.divider()
    st.title('Performance chart')
    chart_data = pd.DataFrame(data)
    chart_data.sort_values(by='TIMESTAMP HISTORY', ascending=True)
    st.area_chart(chart_data, y='TIMESTAMP HISTORY')
