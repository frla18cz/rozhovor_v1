import mysql.connector
import toml
import os
# Load the configuration file
def local_db_login():
    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to secrets.toml relative to the current script
    config_path = os.path.join(dir_path, "../../secrets.toml")

    # Load the TOML file
    config = toml.load(config_path)
    db_user = config["database"]["user"]
    db_pass = config["database"]["password"]
    db_host = config["database"]["host"]
    db_port = config["database"]["port"]
    db_database = config["database"]["database"]

    try:
        cnx = mysql.connector.connect(user=db_user,
                                      password=db_pass,
                                      host=db_host,
                                      port=db_port,
                                      database=db_database)
        mycursor = cnx.cursor()
        query = "SELECT * FROM table_rozhovor ORDER BY id DESC LIMIT 1"
        mycursor.execute(query)

        myresult = mycursor.fetchall()
        print(f"Připojili jsme se lokálně k databázi: {db_database}\ntestovací výpis:{myresult}")
        mycursor = cnx.cursor()



    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    return cnx, mycursor