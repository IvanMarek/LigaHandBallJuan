import sqlite3
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ClubesABM:
    def __init__(self, menu_root):
        self.menu_root = menu_root  # Guardamos la referencia a la ventana del menú
        self.root = tk.Tk()
        self.root.title("Registro de Clubes de Handball")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        self.root.config(bg="#ff7700")
        self.root.option_add("*Font", "Arial 16 bold")

        # Conexión a la base de datos
        self.conn = sqlite3.connect('ligahandball.db')
        self.cursor = self.conn.cursor()

        # Frame para centrar contenido
        self.frame = tk.Frame(self.root, bg="#d3d3d3")  # Fondo gris claro en el frame
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Etiquetas y entradas de texto
        self.label_nombre = tk.Label(self.frame, text="Nombre del Club:", bg="#d3d3d3", fg="black")
        self.label_nombre.grid(column=0, row=0, padx=15, pady=15)
        self.entry_nombre = tk.Entry(self.frame, width=25)
        self.entry_nombre.grid(column=1, row=0, padx=15, pady=15)

        # Botón para seleccionar foto
        self.label_foto = tk.Label(self.frame, text="Foto:", bg="#d3d3d3", fg="black")
        self.label_foto.grid(column=0, row=1, padx=15, pady=15)
        self.entry_foto = tk.Entry(self.frame, width=25)
        self.entry_foto.config(state="disabled")
        self.entry_foto.grid(column=1, row=1, padx=15, pady=15)
        self.button_foto = tk.Button(self.frame, text="Seleccionar", command=self.seleccionar_foto)
        self.button_foto.grid(column=2, row=1, padx=15, pady=15)

        # Etiqueta para mostrar imagen
        self.label_imagen = tk.Label(self.frame)
        self.label_imagen.grid(column=0, row=2, columnspan=3, padx=15, pady=15)

        # Botones para guardar y volver (fuera del frame y con fondo gris claro)
        self.button_guardar = tk.Button(self.root, text="Guardar", command=self.guardar_club, bg="#d3d3d3")
        self.button_guardar.place(relx=0.4, rely=0.8, anchor="center")  # Posicionarlo fuera del frame

        self.button_volver = tk.Button(self.root, text="Volver", command=self.volver, bg="#d3d3d3")
        self.button_volver.place(relx=0.6, rely=0.8, anchor="center")  # Posicionarlo fuera del frame

    def seleccionar_foto(self):
        archivo = filedialog.askopenfilename(title="Seleccionar foto", filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if archivo:  # Comprobar si se seleccionó un archivo
            self.entry_foto.config(state="normal")
            self.entry_foto.delete(0, tk.END)
            self.entry_foto.insert(0, archivo)
            self.entry_foto.config(state="disabled")
            imagen = Image.open(archivo)
            imagen.thumbnail((200, 200))  # Cambiar tamaño de la imagen para mostrarla
            self.imagen_tk = ImageTk.PhotoImage(imagen)
            self.label_imagen.config(image=self.imagen_tk)

    def guardar_club(self):
        nombre = self.entry_nombre.get()
        foto = self.entry_foto.get()
        
        # Verificar que los campos no estén vacíos
        if not nombre:
            tk.messagebox.showwarning("Advertencia", "El nombre del club no puede estar vacío.")
            return
        
        try:
            with self.conn:
                self.cursor.execute("INSERT INTO clubes (nombre, foto) VALUES (?, ?)", (nombre, foto))
                tk.messagebox.showinfo("Éxito", "Club registrado exitosamente.")
                self.entry_nombre.delete(0, tk.END)  # Limpiar campo de nombre
                self.entry_foto.config(state="normal")
                self.entry_foto.delete(0, tk.END)  # Limpiar campo de foto
                self.entry_foto.config(state="disabled")
                self.label_imagen.config(image='')  # Limpiar imagen
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"No se pudo registrar el club: {e}")

    def volver(self):
        self.root.destroy()  # Cerrar la ventana actual
        self.menu_root.deiconify()  # Volver a mostrar la ventana del menú

    def run(self):
        self.root.mainloop()

# Código para lanzar la aplicación
if __name__ == "__main__":
    root_menu = tk.Tk()
    root_menu.withdraw()  # Ocultar ventana del menú al iniciar
    app = ClubesABM(root_menu)
    app.run()
