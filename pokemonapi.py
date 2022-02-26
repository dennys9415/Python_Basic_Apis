import requests
import json
import psycopg2

url = "https://pokeapi.co/api/v2/"

#variables
endpoint="pokemon/"
pokemon = "snorlax"

var1=input("Enter the name of the pokemon: ")


evolution="evolution-chain/"
id_const="7"

#api GET
x = requests.get(url+endpoint+pokemon)
y = requests.get(url+evolution+id_const)
z = requests.get(url+endpoint+var1)
print(x.status_code)
#print(x.text)
#print (x.key[0])
#filter



key= json.loads(z.text)['id']
moves= json.loads(z.text)['moves'][0]["move"]["name"]
id= json.loads(z.text)['id']
height= json.loads(z.text)['height']
#print(moves['name'])
#print("this pokemon "+pokemon+" use this move "+moves)

print ("the pokemon that you've choseen is: "+var1+" whit the id of: "+str(id)+" has used the move : "+moves)
'''
a=int(id)
b=str(height)
c=str(pokemon)
d=str(moves)
pokemon_tuple =(a,b,c,d)
'''

conn = psycopg2.connect(host='172.18.0.2',
                        user='postgres',
                        password='postgres',
                        database='pokemon')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#POST

query = "INSERT INTO data (id, move, heigh, name) VALUES (%s,%s,%s,%s)"
#pokevalue = (id, moves, height, pokemon)
pokevalue = (id, moves, height, var1)
#cursor.execute(query,pokemon_tuple)
cursor.execute(query,pokevalue)
conn.commit()
print("done")



#UPDATE
'''
update_query = """Update data set name = %s where id = %s"""
cursor.execute(update_query)
conn.commit()
count = cursor.rowcount
print(count, "Record updated successfully ")
'''

#DELETE
'''
delete_query = "Delete from data where id = %s"
id_delete=(id,)
cursor.execute(delete_query,id_delete)
conn.commit()
print("deleted")
'''

#DISCONNECT

cursor.close()
conn.close()
