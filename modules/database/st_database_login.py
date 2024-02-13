import mysql.connector
import streamlit as st
def get_database_connection():
    return mysql.connector.connect(
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        database=st.secrets["database"]["database"]
    )