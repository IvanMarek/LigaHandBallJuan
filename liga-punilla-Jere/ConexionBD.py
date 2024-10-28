import tkinter as tk
from tkinter import messagebox
import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root", #PONER SU PROPIO USUARIO
        password="Ivan08012000@", #PONER SU PROPIA CLAVE
        port = 3305,
        database="LigaHandball")
mycursor = mydb.cursor()


