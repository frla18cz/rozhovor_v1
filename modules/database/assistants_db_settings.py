import mysql.connector
import streamlit as st

cnx = mysql.connector.connect(
    user=st.secrets["database"]["user"],
    password=st.secrets["database"]["password"],
    host=st.secrets["database"]["host"],
    port=st.secrets["database"]["port"],
    database=st.secrets["database"]["database"]
)
def get_assistants():
    """Získává seznam dostupných assistantů z databáze."""
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM assistants")
    return cursor.fetchall()

def get_assistant_by_id(id):
    """Získává konkrétního assistenta podle ID."""
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM assistants WHERE id = %s", (id,))
    return cursor.fetchone()

def add_assistant(id, assistants_id, name, instructions, date_created):
    """Přidává nového assistenta do databáze."""
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO assistants (id, assistants_id, name, instructions, date_created) VALUES (%s, %s, %s, %s, %s)", (id, assistants_id, name, instructions, date_created))
    cnx.commit()
    return cursor.lastrowid

# rozpracováno
# def update_assistant(id, assistants_id, name, instructions, date_created):
#     """Aktualizuje existujícího assistenta."""
#     cursor = cnx.cursor()
#     cursor.execute("UPDATE assistants SET name = %s, instructions = %s, config = %s WHERE id = %s", (name, description, assistant_id))
#     cnx.commit()

def delete_assistant(id):
    """Odstraňuje assistenta z databáze."""
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM assistants WHERE id = %s", (id,))
    cnx.commit()
