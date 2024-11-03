import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import os

class PDFViewer:
    PDF_PREDEFINIDO = "C:/Users/Usuario/Downloads/liga-punilla-Jere/REGLAMENTO.pdf"  # Cambia esto por la ruta de tu PDF
    ARCHIVO_RUTA_PDF = "ruta_pdf.txt"

    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de PDF")
        self.root.geometry("400x200")
        self.root.configure(bg="#ff7700")
        
        # Botón para abrir el reglamento
        tk.Button(self.root, text="Abrir Reglamento", command=self.crear_ventana_reglamento).pack(pady=20)
        
        # Variables para archivo PDF y página actual
        self.archivo_pdf = None
        self.pagina_actual = 0
        self.etiqueta_imagen = None
        self.etiqueta_estado = None

    def cargar_ruta_pdf(self):
        """Cargar la ruta del último PDF guardado desde un archivo."""
        if os.path.exists(self.ARCHIVO_RUTA_PDF):
            with open(self.ARCHIVO_RUTA_PDF, "r") as file:
                return file.read().strip()
        return self.PDF_PREDEFINIDO

    def guardar_ruta_pdf(self, ruta):
        """Guardar la ruta del PDF actual en un archivo."""
        with open(self.ARCHIVO_RUTA_PDF, "w") as file:
            file.write(ruta)

    def abrir_pdf(self, archivo_pdf):
        """Abrir un archivo PDF y mostrar la primera página."""
        try:
            self.archivo_pdf = fitz.open(archivo_pdf)
            self.pagina_actual = 0
            self.mostrar_pagina(self.pagina_actual)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el PDF: {str(e)}")

    def mostrar_pagina(self, num_pagina):
        """Mostrar la página especificada del PDF."""
        try:
            if 0 <= num_pagina < len(self.archivo_pdf):
                pagina = self.archivo_pdf.load_page(num_pagina)
                pix = pagina.get_pixmap()
                imagen = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                imagen_tk = ImageTk.PhotoImage(imagen)

                self.etiqueta_imagen.image = imagen_tk  # Mantener la referencia
                self.etiqueta_imagen.config(image=imagen_tk)  # Actualizar la imagen mostrada
                self.actualizar_estado_pagina()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar la página: {str(e)}")

    def actualizar_estado_pagina(self):
        """Actualizar el estado de la página actual en la etiqueta."""
        self.etiqueta_estado.config(text=f"Página {self.pagina_actual + 1} de {len(self.archivo_pdf)}")

    def pagina_anterior(self):
        """Navegar a la página anterior del PDF."""
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.mostrar_pagina(self.pagina_actual)

    def pagina_siguiente(self):
        """Navegar a la página siguiente del PDF."""
        if self.pagina_actual < len(self.archivo_pdf) - 1:
            self.pagina_actual += 1
            self.mostrar_pagina(self.pagina_actual)

    def volver(self, ventana):
        """Cerrar la ventana actual y volver al menú."""
        ventana.destroy()

    def seleccionar_pdf(self):
        """Abrir un cuadro de diálogo para seleccionar un nuevo PDF."""
        nuevo_pdf = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
        if nuevo_pdf:
            self.abrir_pdf(nuevo_pdf)
            self.guardar_ruta_pdf(nuevo_pdf)

    def guardar_pdf(self):
        """Abrir un cuadro de diálogo para guardar el PDF actual."""
        if self.archivo_pdf:
            guardar_como = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
            if guardar_como:
                self.archivo_pdf.save(guardar_como)
                messagebox.showinfo("Guardado", "PDF guardado con éxito.")
                self.guardar_ruta_pdf(guardar_como)

    def crear_ventana_reglamento(self):
        """Crear una nueva ventana para mostrar el reglamento."""
        ventana_reglamento = tk.Toplevel()
        ventana_reglamento.title("Reglamento de la Liga")
        ventana_reglamento.geometry("1365x768")
        ventana_reglamento.configure(bg="#ff7700")
        
        # Crear área para mostrar el PDF
        self.etiqueta_imagen = tk.Label(ventana_reglamento)
        self.etiqueta_imagen.pack(expand=True, fill="both")

        # Frame para los botones de navegación
        frame_botones = tk.Frame(ventana_reglamento, bg="#ff7700")
        frame_botones.pack(side="right", padx=10, pady=10, fill="y")

        # Botones de la interfaz
        tk.Button(frame_botones, text="Seleccionar PDF", command=self.seleccionar_pdf).pack(pady=5)
        tk.Button(frame_botones, text="Guardar PDF", command=self.guardar_pdf).pack(pady=5)
        tk.Button(frame_botones, text="Página Anterior", command=self.pagina_anterior).pack(pady=5)
        self.etiqueta_estado = tk.Label(frame_botones, text="Página 1 de 1", bg="#ff7700")
        self.etiqueta_estado.pack(pady=5)
        tk.Button(frame_botones, text="Página Siguiente", command=self.pagina_siguiente).pack(pady=5)
        tk.Button(frame_botones, text="Volver", command=lambda: self.volver(ventana_reglamento)).pack(pady=5)

        # Cargar automáticamente el PDF guardado al iniciar el programa
        ruta_pdf_guardado = self.cargar_ruta_pdf()
        self.abrir_pdf(ruta_pdf_guardado)

# Ejecutar el visualizador de PDF
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = PDFViewer(ventana_principal)
    ventana_principal.mainloop()
