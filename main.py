import mysql.connector
import toml
from modules.database.local_database_login import local_db_login
debug_mode = True

if debug_mode == True:
    print("Debug mode is on")
    cnx, mycursor = local_db_login()  # Přiřazení výstupů funkce do proměnných
else:
    print("Debug mode is off")
    print("No local database connection")
print(cnx)
print(mycursor)