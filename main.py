import tkinter as tk
from tkinter import ttk, messagebox

# Importamos nuestros propios módulos
from modelo import BaseDeDatos
from vistas import TabComercial, TabRiesgos, TabOperaciones, TabConsultas

class AppControlador:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Préstamos")
        self.root.geometry("800x500")

        # Inicializar el Modelo (Datos)
        self.db = BaseDeDatos()

        # Inicializar las Vistas (Notebook / Pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Crear y agregar las pestañas inyectando el controlador (self)
        self.tab_comercial = TabComercial(self.notebook, self)
        self.tab_riesgos = TabRiesgos(self.notebook, self)
        self.tab_operaciones = TabOperaciones(self.notebook, self)

        self.notebook.add(self.tab_comercial, text="Ejecutivo Comercial")
        self.notebook.add(self.tab_riesgos, text="Analista de Riesgos")
        self.notebook.add(self.tab_operaciones, text="Operaciones")
        self.tab_consultas = TabConsultas(self.notebook, self)
        self.notebook.add(self.tab_consultas, text="Base de Datos")

    # --- Lógica de Coordinación (El controlador decide qué hacer) ---
    def registrar_cliente(self, dni, nombre):
        exito, msj = self.db.registrar_cliente(dni, nombre)
        if exito:
            messagebox.showinfo("Éxito", msj)
        else:
            messagebox.showerror("Error", msj)

    def crear_solicitud(self, dni, monto, plazo):
        exito, msj = self.db.crear_solicitud(dni, monto, plazo)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.refrescar_vistas() # Avisar a las tablas que hay datos nuevos
        else:
            messagebox.showerror("Error", msj)

    def procesar_solicitud(self, id_solicitud, estado):
        if self.db.actualizar_estado_solicitud(id_solicitud, estado):
            messagebox.showinfo("Éxito", f"Solicitud {id_solicitud} actualizada a: {estado}")
            self.refrescar_vistas()

    def ejecutar_desembolso(self, id_solicitud):
        exito, msj = self.db.desembolsar_prestamo(id_solicitud)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.refrescar_vistas()
        else:
            messagebox.showerror("Error", msj)

    def refrescar_vistas(self):
        # 1. Obtener todos los datos desde Supabase
        solicitudes = self.db.obtener_solicitudes()
        clientes = self.db.obtener_clientes()
        prestamos = self.db.obtener_prestamos()

        # 2. Actualizar las tablas normales
        self.tab_riesgos.actualizar_tabla(solicitudes)
        self.tab_operaciones.actualizar_tabla(solicitudes)
        
        # 3. Actualizar la pestaña de Debug
        self.tab_consultas.actualizar_datos(clientes, solicitudes, prestamos)

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = AppControlador(ventana_principal)
    ventana_principal.mainloop()