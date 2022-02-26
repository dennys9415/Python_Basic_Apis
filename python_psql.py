import psycopg2

host = 'localhost'
database = 'postgres'
user = 'postgres'
password = 'postgres'
port = '3306'

conn= None
cur= None
try:
#establishing the connection
    conn = psycopg2.connect(
       database=database, user=user, password=password, host=host, port=port
    )
#Creating a cursor object using the cursor() method
    cursor = conn.cursor()

#Executing an MYSQL function using the execute() method
    cursor.execute("select version()")

# Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print("Connection established to: ",data)


except Exception as error:
    print(error)

finally:
#Closing the connection
    if cur is not None:
        cursor.close()
    if conn is not None:
        conn.close()