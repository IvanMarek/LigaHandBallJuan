
import mysql.connector

# Configuración de la conexión a la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="",
    port="3305", 
    database="liga_handball"
)

mycursor = mydb.cursor()  # type: ignore
