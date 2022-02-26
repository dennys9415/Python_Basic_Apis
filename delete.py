import mysql.connector
from mysql.connector import Error
from os import path
import os
from dotenv import load_dotenv

# Variables from .env 
load_dotenv()
HOST = os.getenv("host")
DATABASE= os.getenv("database")
USER = os.getenv("user")
PASSWORD = os.getenv("password")
PORT = os.getenv("port")

# Variables to connecto to MySql DB 
host = HOST
database = DATABASE
user = USER
password = PASSWORD
port = PORT 

def MethodDelete():
    id_to_delete=input("Enter the ID of the voicemail which you want to delete: ")

    delete_query = "Delete from ast_voicemessages where msg_id = %s"
    id_delete=(id_to_delete,)
    cursor.execute(delete_query,id_delete)
    conn.commit()
    print("deleted")
    
try:
#establishing the connection to DB
    conn = mysql.connector.connect(
       database=database, user=user, password=password, host=host, port=port
    )
#Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    MethodDelete()         #well done
    
#Error and Closing connexion
except Exception as error:
    print(error)
finally:
    if (conn.is_connected()):
        cursor.close()
        conn.close()
        print("Work done and the connection is closed")