import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import mysql.connector


class ListaAutoridadesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Autoridades")
        self.root.state('zoomed')
        self.root.resizable(False, False)
        self.root.configure(bg="#ff7700")

        self.setup_ui()
        self.actualizar_treeview()

    def setup_ui(self):
        # Título
        label = tk.Label(self.root, text="Autoridades Registradas", font=("Calibri", 24), bg="#ff7700")
        label.pack(pady=(20, 10))

        # Frame para filtro de puesto
        frame_filtro = tk.Frame(self.root, bg="#ff7700")
        frame_filtro.pack(pady=(10, 0))

        tk.Label(frame_filtro, text="Filtrar por puesto:", font=("Calibri", 18), bg="#ff7700").pack(side=tk.LEFT, padx=10)

        # Combobox para seleccionar el puesto
        puestos = self.obtener_puestos()
        puestos.insert(0, "Todos")

        self.slider_filtro = ttk.Combobox(frame_filtro, values=puestos, state="readonly", font=("Calibri", 18))
        self.slider_filtro.current(0)
        self.slider_filtro.pack(side=tk.LEFT)

        # Botón de filtro
        button_filtrar = tk.Button(frame_filtro, text="Aplicar Filtro", font=("Calibri", 18), bg="#d3d3d3", command=self.actualizar_treeview)
        button_filtrar.pack(side=tk.LEFT, padx=10)

        # Treeview para mostrar las autoridades
        self.arbol = ttk.Treeview(self.root, columns=("nombre", "apellido", "puesto"), show="headings")
        self.arbol.pack(pady=(10, 20), expand=True, fill='both')

        self.arbol.heading("nombre", text="Nombre")
        self.arbol.heading("apellido", text="Apellido")
        self.arbol.heading("puesto", text="Puesto")
        self.arbol.column("nombre", anchor='center', width=200)
        self.arbol.column("apellido", anchor='center', width=200)
        self.arbol.column("puesto", anchor='center', width=150)

        # Frame para botones de acción
        button_frame = tk.Frame(self.root, bg="#ff7700")
        button_frame.pack(pady=(20, 20))

        # Botón "Volver"
        button_volver = tk.Button(button_frame, text="Volver", font=("Calibri", 24), bg="#d3d3d3", command=self.volver_menu)
        button_volver.pack(side=tk.LEFT, padx=(0, 20))

        # Puedes descomentar los botones según los necesites
        # Botón "Agregar" - para añadir una nueva autoridad
        button_nuevo = tk.Button(button_frame, text="Agregar", font=("Calibri", 24), bg="#d3d3d3", command=self.nueva_autoridad)
        button_nuevo.pack(side=tk.LEFT, padx=(0, 20))

        #Botón "Modificar" - para modificar una autoridad seleccionada
        button_modificar = tk.Button(button_frame, text="Modificar", font=("Calibri", 24), bg="#d3d3d3", command=self.modificar_autoridad)
        button_modificar.pack(side=tk.LEFT, padx=(0, 20))

        # Botón "Registrar Autoridades" - para ir a la interfaz de RegistrarAutoridades
        button_registrar = tk.Button(button_frame, text="Registrar Autoridades", font=("Calibri", 24), bg="#d3d3d3", command=self.registrar_autoridades)
        button_registrar.pack(side=tk.LEFT)

    def obtener_autoridades(self, filtro_puesto=None):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Asegúrate de tener la contraseña correcta
                database="LigaHandball"
            )
            cursor = conn.cursor()
            if filtro_puesto and filtro_puesto != "Todos":
                cursor.execute("""
                    SELECT A.nombre, A.apellido, P.nombre AS puesto
                    FROM Autoridades A
                    JOIN Puestos P ON A.puesto_id = P.id
                    WHERE P.nombre = %s
                """, (filtro_puesto,))
            else:
                cursor.execute("""
                    SELECT A.nombre, A.apellido, P.nombre AS puesto
                    FROM Autoridades A
                    JOIN Puestos P ON A.puesto_id = P.id
                """)
            autoridades_bd = cursor.fetchall()
            return autoridades_bd
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo obtener la lista de autoridades: {e}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def obtener_puestos(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Asegúrate de tener la contraseña correcta
                database="LigaHandball"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM Puestos")
            puestos = [puesto[0] for puesto in cursor.fetchall()]
            return puestos
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo obtener la lista de puestos: {e}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def modificar_autoridad(self):
        selected_index = self.arbol.selection()
        if selected_index:
            autoridad_actual = self.arbol.item(selected_index[0])['values'][0]
            nuevo_nombre = simpledialog.askstring("Modificar Autoridad", "Ingrese el nuevo nombre:", initialvalue=autoridad_actual)
            if nuevo_nombre:
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",  # Asegúrate de tener la contraseña correcta
                        database="LigaHandball"
                    )
                    cursor = conn.cursor()
                    cursor.execute("UPDATE Autoridades SET nombre = %s WHERE nombre = %s", (nuevo_nombre, autoridad_actual))
                    conn.commit()
                    self.actualizar_treeview()
                    messagebox.showinfo("Éxito", "Los datos de la autoridad han sido modificados con éxito.")
                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"No se pudo modificar la autoridad: {e}")
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()

    def volver_menu(self):
        self.root.destroy()
        import Menu

    def nueva_autoridad(self):
        self.root.destroy()
        import RegistrarAutoridad

    def registrar_autoridades(self):
        self.root.destroy()
        import RegistrarAutoridades

    def actualizar_treeview(self):
        for item in self.arbol.get_children():
            self.arbol.delete(item)
        filtro_puesto = self.slider_filtro.get()
        autoridades_bd = self.obtener_autoridades(filtro_puesto if filtro_puesto and filtro_puesto != "Todos" else None)
        for autoridad in autoridades_bd:
            self.arbol.insert("", "end", values=(autoridad[0], autoridad[1], autoridad[2]))

if __name__ == "__main__":
    root = tk.Tk()
    app = ListaAutoridadesApp(root)
    root.mainloop()
