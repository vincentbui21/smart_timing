import mysql.connector
import pandas as pd
import streamlit as st

db = mysql.connector.connect(
    host = 'localhost',
    user = 'admin',
    password = '123',
    database = 'std'
)

mycursor = db.cursor()

def create_new_runner(name:str, id:int):

    name = name.upper() #Change the name input to all caps

    sql_formula = 'INSERT INTO runners (name, id) VALUES (%s, %s)'
    new_runner = (name,id)

    mycursor.execute(sql_formula, new_runner)
    db.commit()

def new_command(command:str):
    mycursor.execute(command)
    db.commit()

def select_database(database_name:str, col: str = '*', condition: str = None,fetch_all:bool = True, print_result:bool = False):
    if condition == None:
        mycursor.execute(f'SELECT {col} FROM {database_name}')
    else:
        mycursor.execute(f'SELECT {col} FROM {database_name} WHERE {condition}')

    if fetch_all:
        result = mycursor.fetchall()
    else:
        result = mycursor.fetchone()

    if print_result:
        for row in result:
            print(row)
    else:
        temp_tuple = []
        for row in result:
            if len(row) == 1:
                temp_tuple.append(row[0])  
            else:
                return result            
        return tuple(temp_tuple)
    
def add_new_timestamp(timestamp:str, runner_id:int):
    sql_formula = 'INSERT INTO timestamphistory (timestamp, runner_id) VALUES (%s, %s)'

    new_timestamp = (timestamp, runner_id)

    mycursor.execute(sql_formula, new_timestamp)
    db.commit()

def get_runner_name(devide:bool= False):
    mycursor.execute('SELECT name, id from runners')
    result = mycursor.fetchall()

    temp_tuple_name = []
    temp_tuple_id = []
    temp_tuple_mix_name_id=[]
    if devide:
        for row in result:
            temp_tuple_name.append(row[0])
            temp_tuple_id.append(row[1])
            temp_tuple_mix_name_id.append(f'Name: {row[0]} - ID: {row[1]}')
        return tuple(temp_tuple_name), tuple(temp_tuple_id), tuple(temp_tuple_mix_name_id)
    else:
        return result


if __name__ == '__main__':
    option = st.selectbox(
    "Choose runner's name to see/update data",
    select_database('runners', col="name"),
    index= 0,
    )
    st.divider()

    mycursor.execute(f'SELECT timestamp FROM timestamphistory LEFT JOIN runners ON timestamphistory.runner_id = runners.id WHERE name ="{option}"')
    result = mycursor.fetchall()
    pf = pd.DataFrame(result)
    pf.columns = ['Timestamp']
    st.dataframe(pf, hide_index=True, height=500)
