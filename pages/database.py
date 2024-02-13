import streamlit as st
import mysql.connector
from modules.database.local_database_login import local_db_login

def database_page_show():
    st.title("Databáze")
    st.write("Testování funkčnosti databáze.")
    # Další kód specifický pro stránku "Databáze"

    try:
        cnx = mysql.connector.connect(user=st.secrets["database"]["user"],
                                      password=st.secrets["password"],
                                      host=st.secrets["database"]["host"],
                                      port=st.secrets["database"]["port"],
                                      database=st.secrets["database"]["database"])
        mycursor = cnx.cursor()
        query = "SELECT * FROM table_rozhovor ORDER BY id DESC LIMIT 1"
        mycursor.execute(query)

        myresult = mycursor.fetchall()
        st.write(f"Připojili jsme se k databázi přes cloud streamlit: {st.secrets["database"]["database"]}\ntestovací výpis:{myresult}")
        mycursor = cnx.cursor()



    except mysql.connector.Error as err:
        st.write("Something went wrong: {}".format(err))
    return cnx, mycursor