import mysql.connector
from mysql.connector import Error
import speech_recognition as sr
import sys
from os import path
import os
from dotenv import load_dotenv
import audioread

file=sys.argv[1]
dirFile=sys.argv[2]

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

# GOOGLE API Speech_To_Text
def SpeechoToText():
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)),dirFile+"/"+file)
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
    text_audio=r.recognize_google(audio)
    return (text_audio)

# Function Convert to Binary to store as a Blob
def ConvertToBinary(filename):
    with open(filename,'rb') as file:
        binarydata=file.read()
    return binarydata

# Function to get the duration of a file
def duration_detector(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds
    return hours, mins, seconds
# f is the fileobject being created
def DurationAudio():
    with audioread.audio_open(file) as f:
        # totalsec contains the length in float
        totalsec = f.duration
        hours, mins, seconds = duration_detector(int(totalsec))
        print('Total Duration: {}:{}:{}'.format(hours, mins, seconds))
        time_traveler=('{}:{}:{}'.format(hours, mins, seconds))
        return (time_traveler)
    
def MethodPost():
    # Variables from the Bash Script (Audio_encoding.sh)
    
#    insert_query = """insert into ast_voicemessages (audioname,dir,recording,duration,lastmodify) value (%s,%s,%s,%s,CURTIME())"""
    
    insert_query = """insert into ast_voicemessages (audioname,dir,txtrecording,recording,duration,lastmodify) value (%s,%s,%s,%s,%s,CURTIME())"""
    duration_audio=DurationAudio()
    audio_total=SpeechoToText()
    convertFile=ConvertToBinary(dirFile+"/"+file)
#    value=(file,dirFile,convertFile,duration_audio)
    value=(file,dirFile,audio_total,convertFile,duration_audio)
    cursor.execute(insert_query,value)
    conn.commit()
    
try:
#establishing the connection to DB
    conn = mysql.connector.connect(
       database=database, user=user, password=password, host=host, port=port
    )
#Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    MethodPost()
    
#Error and Closing connexion
except Exception as error:
    print(error)
finally:
    if (conn.is_connected()):
        cursor.close()
        conn.close()
        print("Work done and the connection is closed")

