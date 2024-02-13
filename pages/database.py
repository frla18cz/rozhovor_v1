import streamlit as st
import mysql.connector
import pandas as pd
from modules.database.st_database_login import get_database_connection
from modules.database.assistants_db_settings import get_assistants, get_assistant_by_id

st.title("Databáze - Test")

assistants = get_assistants()
if assistants:  # Zkontrolujte, zda existují nějací asistenti
    # Vytvoření seznamu názvů asistentů s předvolbou "Vyberte..."
    assistant_names = ["Vyberte..."] + [assistant['name'] for assistant in assistants]

    # Necháme uživatele vybrat asistenta podle jména
    selected_name = st.selectbox("Vyberte assistenta:", options=assistant_names)

    if selected_name != "Vyberte...":
        # Získání informací o vybraném asistentovi na základě jména
        selected_assistant = next((assistant for assistant in assistants if assistant['name'] == selected_name), None)

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
        st.write("Vyberte asistenta z nabídky.")
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

