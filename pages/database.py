import streamlit as st
import mysql.connector


# Předpokládám, že `local_db_login` je funkce nebo proměnná, kterou zde nepoužíváte, takže ji z příkladu vynechávám.

def database_page_show():
    st.title("Databáze")
    st.write("Testování funkčnosti databáze.")

    # Tlačítko pro spuštění databázového dotazu
    if st.button('Zobrazit poslední záznam'):
        try:
            cnx = mysql.connector.connect(
                user=st.secrets["database"]["user"],
                password=st.secrets["database"]["password"],
                host=st.secrets["database"]["host"],
                port=st.secrets["database"]["port"],
                database=st.secrets["database"]["database"]
            )
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

