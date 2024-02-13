import streamlit as st
import mysql.connector
import pandas as pd
from modules.database.st_database_login import get_database_connection
from modules.database.assistants_db_settings import get_assistants, get_assistant_by_id

st.title("Databáze - Test")

assistants = get_assistants()
if assistants:  # Zkontrolujte, zda existují nějací asistenti
    assistant_options = {assistant['name']: assistant['id'] for assistant in assistants}
    selected_assistant_id = st.selectbox("Vyberte assistenta:", options=[0] + list(assistant_options.values()), format_func=lambda x: assistant_options.get(x, "Vyberte..."))
    if selected_assistant_id != 0:
        if st.button("Zobrazit informace"):
            selected_assistant = get_assistant_by_id(selected_assistant_id)

            if selected_assistant:
                # Příprava dat pro zobrazení
                assistant_data = {
                    "ID": [selected_assistant["id"]],
                    "Jméno": [selected_assistant["name"]],
                    "Instructions": [selected_assistant["instructions"]],
                }

                # Konverze dat do DataFrame pro lepší zobrazení v Streamlit
                assistant_df = pd.DataFrame(assistant_data)

                # Zobrazení tabulky s informacemi o asistentovi
                st.table(assistant_df)
    else:
        st.write("Nejprve vyberte asistenta.")
else:
    st.write("Nebyli nalezeni žádní asistenti.")

def database_page_show():
    st.title("Databáze")
    st.write("Testování funkčnosti databáze.")

    # Tlačítko pro spuštění databázového dotazu
    if st.button('Zobrazit poslední záznam'):
        try:
            # cnx = mysql.connector.connect(
            #     user=st.secrets["database"]["user"],
            #     password=st.secrets["database"]["password"],
            #     host=st.secrets["database"]["host"],
            #     port=st.secrets["database"]["port"],
            #     database=st.secrets["database"]["database"]
            # )

            cnx = get_database_connection()
            mycursor = cnx.cursor()
            query = "SELECT * FROM table_rozhovor ORDER BY id DESC LIMIT 1"
            mycursor.execute(query)

            myresult = mycursor.fetchall()
            if myresult:
                st.write("Připojili jsme se k databázi přes cloud streamlit.")
                st.write("Název databáze:", st.secrets["database"]["database"])
                st.write("Testovací výpis:", myresult)
            else:
                st.write("Žádné záznamy nebyly nalezeny.")

            mycursor.close()
            cnx.close()

        except mysql.connector.Error as err:
            st.write("Something went wrong: {}".format(err))

