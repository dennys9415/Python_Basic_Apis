import mysql.connector
from mysql.connector import Error
import speech_recognition as sr
import sys
from os import path
import os
from dotenv import load_dotenv
import audioread

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

# Function to Download BLOB from Mysql
def WriteFile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as f:
        f.write(data)

    
def MethodPut():
    global file
    file="temporaryfile.wav"
    global dirFile
    dirFile=os.getcwd()

    #id_to_download=input("Enter the ID of the voicemail which you want to update the audio text: ")
   
    download_query = "select recording from ast_voicemessages where msg_id=%s"
    cursor.execute(download_query,(id_to_download,))
    photo = cursor.fetchone()[0]
    WriteFile(photo, file)
    os.system("ffmpeg -i temporaryfile.wav temporaryfile_new.wav")
    file_draft=file
    file="temporaryfile_new.wav"
    
    #CONDITIONAL FOR THE DURATION OF THE AUDIO
    duration_audio=DurationAudio()
    print(duration_audio)
    a="0:0:3"
    if duration_audio < a:
        #print("duration time is less than 5 seconds")
        audio_total=""
    else:
        #print("Its more than 5 seconds")
        audio_total=SpeechoToText()
       
    update_query= """update ast_voicemessages set txtrecording=%s,duration=%s,audioname=%s,lastmodify=CURTIME() where msg_id=%s"""
    new_audioname="Audio_"+id_to_download
    id_update=(audio_total,duration_audio,new_audioname,id_to_download)    
    cursor.execute(update_query,id_update)
    conn.commit()

    os.remove(file_draft)
    os.remove(file)

def MethodUpdateAll():
    
    update_all_query="select msg_id from ast_voicemessages where txtrecording IS NULL"
    cursor.execute(update_all_query)
    data = cursor.fetchall()
    print(data)

    for r in data:
        d=r[0]
        print(d)
        global id_to_download
        id_to_download=str(d)
        MethodPut()

try:
#establishing the connection to DB
    conn = mysql.connector.connect(
       database=database, user=user, password=password, host=host, port=port
    )
#Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    MethodUpdateAll()
    
#Error and Closing connexion
except Exception as error:
    print(error)
finally:
    if (conn.is_connected()):
        cursor.close()
        conn.close()
        print("Work done and the connection is closed")