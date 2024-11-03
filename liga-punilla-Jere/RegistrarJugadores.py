import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import re

class FormularioJugadores:
    def __init__(self, root):
        self.root = root
        self.root.title("Alta/Modificación de Jugadores")
        self.root.geometry("1366x765")
        self.root.configure(bg="#ff7f00")
        self.root.resizable(False, False)
        
        # Directorio de imágenes
        self.directorio_imagenes = r"C:\Users\Usuario\Downloads\visual code\matematica\Liga de Handball Punilla"
        
        # Inicializar interfaz gráfica
        self.configurar_interfaz()
        
    def configurar_interfaz(self):
        # Frames
        self.frame_datos = tk.Frame(self.root, bg="#ff7f00")
        self.frame_datos.grid(row=0, column=0, padx=50, pady=20, sticky="n")

        self.frame_imagenes = tk.Frame(self.root, bg="#ff7f00")
        self.frame_imagenes.grid(row=0, column=1, padx=50, pady=20, sticky="n")

        self.frame_botones = tk.Frame(self.root, bg="#ff7f00")
        self.frame_botones.grid(row=1, column=0, columnspan=2, padx=20, pady=40, sticky="n")

        # Campos de entrada
        self.entry_nombre = tk.Entry(self.frame_datos, width=30, validate="key")
        self.entry_nombre['validatecommand'] = (self.root.register(self.solo_letras), '%S')
        self.entry_nombre.grid(row=1, column=1, pady=5)

        self.entry_apellido = tk.Entry(self.frame_datos, width=30, validate="key")
        self.entry_apellido['validatecommand'] = (self.root.register(self.solo_letras), '%S')
        self.entry_apellido.grid(row=2, column=1, pady=5)

        self.entry_dni = tk.Entry(self.frame_datos, width=30, validate="key")
        self.entry_dni['validatecommand'] = (self.root.register(self.solo_numeros), '%S')
        self.entry_dni.grid(row=3, column=1, pady=5)

        self.entry_domicilio = tk.Entry(self.frame_datos, width=30)
        self.entry_domicilio.grid(row=4, column=1, pady=5)

        self.entry_telefono = tk.Entry(self.frame_datos, width=30, validate="key")
        self.entry_telefono['validatecommand'] = (self.root.register(self.solo_numeros), '%S')
        self.entry_telefono.grid(row=5, column=1, pady=5)

        self.entry_correo = tk.Entry(self.frame_datos, width=30)
        self.entry_correo.grid(row=6, column=1, pady=5)

        self.entry_fecha_nacimiento = DateEntry(self.frame_datos, width=27, background="orange", foreground="black", date_pattern="dd-mm-yyyy", state="readonly")
        self.entry_fecha_nacimiento.set_date('23-10-2024')
        self.entry_fecha_nacimiento.grid(row=7, column=1, pady=5)

        # ComboBoxes
        self.localidad_combo = ttk.Combobox(self.frame_datos, values=["Ninguna", "Villa Carlos Paz", "Cosquín", "La Falda", "Huerta Grande"], state='readonly')
        self.localidad_combo.set("Ninguna")
        self.localidad_combo.grid(row=8, column=1, pady=5)

        self.club_combo = ttk.Combobox(self.frame_datos, values=["Cualquiera", "Club 1", "Club 2", "Club 3"], state='readonly')
        self.club_combo.set("Cualquiera")
        self.club_combo.grid(row=9, column=1, pady=5)

        self.tipo_combo = ttk.Combobox(self.frame_datos, values=["Categoría", "Infantil", "Juvenil", "Adulto"], state='readonly')
        self.tipo_combo.set("Categoría")
        self.tipo_combo.grid(row=10, column=1, pady=5)

        # Labels e imágenes en el frame de imágenes
        self.ficha_medica_img_label = tk.Label(self.frame_imagenes, text="Sin Imagen", width=20, height=10, bg="white")
        self.ficha_medica_img_label.pack(pady=10)
        self.carnet_img_label = tk.Label(self.frame_imagenes, text="Sin Imagen", width=20, height=10, bg="white")
        self.carnet_img_label.pack(pady=10)

        tk.Button(self.frame_imagenes, text="Cargar Ficha Médica", command=lambda: self.cargar_imagen(self.ficha_medica_img_label)).pack(pady=5)
        tk.Button(self.frame_imagenes, text="Cargar Carnet", command=lambda: self.cargar_imagen(self.carnet_img_label)).pack(pady=5)

        # Botones de acciones
        tk.Button(self.frame_botones, text="Guardar", command=self.validar_campos).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(self.frame_botones, text="Borrar Datos", command=self.borrar_datos).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.frame_botones, text="Salir", command=self.root.quit).grid(row=0, column=2, padx=10, pady=5)

    def cargar_imagen(self, label):
        archivo = filedialog.askopenfilename(initialdir=self.directorio_imagenes, filetypes=[("Imágenes", ".png;.jpg;*.jpeg")])
        if archivo:
            img = Image.open(archivo)
            label_width = label.winfo_width()
            label_height = label.winfo_height()
            img.thumbnail((label_width, label_height), Image.LANCZOS)
            img = img.resize((label_width, label_height), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            label.config(image=img)
            label.image = img

    def verificar_correo(self, correo):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, correo):
            messagebox.showerror("Error", f"{correo} : no es una dirección de correo válida.")
            return False
        return True

    def validar_dni(self, dni):
        if not dni.isdigit() or not (7 <= len(dni) <= 8):
            messagebox.showerror("Error", "El DNI debe tener 7 u 8 dígitos y contener solo números.")
            return False
        return True

    def validar_telefono(self, telefono):
        if not telefono.isdigit() or not (6 <= len(telefono) <= 10):
            messagebox.showerror("Error", "El teléfono debe tener entre 6 y 10 dígitos y contener solo números.")
            return False
        return True

    def validar_campos_obligatorios(self, entries):
        if any(entry.get().strip() == "" for entry in entries):
            messagebox.showerror("Error", "Todos los campos obligatorios deben completarse.")
            return False
        return True

    def validar_campos(self):
        if not self.validar_campos_obligatorios([self.entry_nombre, self.entry_apellido, self.entry_dni, self.entry_correo]):
            return False
        if not re.match("^[A-Za-z ]+$", self.entry_nombre.get()) or not re.match("^[A-Za-z ]+$", self.entry_apellido.get()):
            messagebox.showerror("Error", "Nombre y apellido deben contener solo letras y espacios.")
            return False
        if not self.validar_dni(self.entry_dni.get()) or not self.validar_telefono(self.entry_telefono.get()):
            return False
        if not self.verificar_correo(self.entry_correo.get()):
            return False
        if self.tipo_combo.get() == 'Categoría' or self.localidad_combo.get() == 'Ninguna' or self.club_combo.get() == 'Cualquiera':
            messagebox.showerror("Error", "Debe seleccionar opciones válidas en categoría, localidad y club.")
            return False
        if not hasattr(self.ficha_medica_img_label, 'image') or not hasattr(self.carnet_img_label, 'image'):
            messagebox.showerror("Error", "Es obligatorio cargar el Carnet y la Ficha Médica.")
            return False
        if messagebox.askyesno("Confirmación", "¿Está seguro que desea guardar los datos?"):
            messagebox.showinfo("Guardado exitoso", "Jugador agregado exitosamente ⚽")
            self.borrar_datos()
            return True
        return False

    def borrar_datos(self):
        for entry in [self.entry_nombre, self.entry_apellido, self.entry_dni, self.entry_domicilio, self.entry_telefono, self.entry_correo]:
            entry.delete(0, tk.END)
        self.entry_fecha_nacimiento.set_date('23-10-2024')
        self.localidad_combo.set("Ninguna")
        self.club_combo.set("Cualquiera")
        self.tipo_combo.set("Categoría")
        self.ficha_medica_img_label.config(image="", text="Sin Imagen")
        self.carnet_img_label.config(image="", text="Sin Imagen")

    def solo_letras(self, char):
        return char.isalpha() or char == " "

    def solo_numeros(self, char):
        return char.isdigit()

if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioJugadores(root)
    root.mainloop()
