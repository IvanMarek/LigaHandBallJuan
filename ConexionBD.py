
import mysql.connector

# Configuración de la conexión a la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="", 
    database="liga_handball"
)

mycursor = mydb.cursor()  # type: ignore
