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

def ConnectionCheck():
    #show the connection
    cursor.execute("select version()")
    data = cursor.fetchone()
    print("Connection established to: ",data)
    
def MethodGet():
    id_to_watch=input("Enter the msg_ID of the voicemail which you're looking for: ")
    get_query= "SELECT msg_id,msgnum,dir,context,macrocontext,callerid,origtime,duration,mailboxuser,mailboxcontext,txtrecording,flag,audioname,lastmodify FROM ast_voicemessages WHERE msg_id=%s"   
    cursor.execute(get_query,(id_to_watch,))
    audiodata = cursor.fetchone()
    print(audiodata)
    #conn.commit()
try:
#establishing the connection to DB
    conn = mysql.connector.connect(
       database=database, user=user, password=password, host=host, port=port
    )
#Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    ConnectionCheck()       ##well done
    MethodGet()            #well done
    
#Error and Closing connexion
except Exception as error:
    print(error)
finally:
    if (conn.is_connected()):
        cursor.close()
        conn.close()
        print("Work done and the connection is closed")