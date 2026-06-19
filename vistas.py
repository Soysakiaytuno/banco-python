import tkinter as tk
from tkinter import ttk, messagebox
# prueba par CI CD 
class TabComercial(ttk.Frame):
    """ Módulo para Ejecutivos Comerciales (HU-01 y HU-02) """
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.crear_widgets()

    def crear_widgets(self):
        # --- HU-01: Registrar Cliente ---
        frame_reg = ttk.LabelFrame(self, text="HU-01: Registrar Cliente")
        frame_reg.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(frame_reg, text="DNI:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_dni = ttk.Entry(frame_reg)
        self.ent_dni.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_reg, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_nombre = ttk.Entry(frame_reg)
        self.ent_nombre.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_reg, text="Guardar Cliente", command=self.on_registrar_cliente).grid(row=2, column=0, columnspan=2, pady=10)

        # --- HU-02: Crear Solicitud ---
        frame_sol = ttk.LabelFrame(self, text="HU-02: Crear Solicitud")
        frame_sol.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(frame_sol, text="DNI Cliente:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_sol_dni = ttk.Entry(frame_sol)
        self.ent_sol_dni.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_sol, text="Monto:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_monto = ttk.Entry(frame_sol)
        self.ent_monto.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_sol, text="Plazo (Meses):").grid(row=2, column=0, padx=5, pady=5)
        self.ent_plazo = ttk.Entry(frame_sol)
        self.ent_plazo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_sol, text="Crear Solicitud", command=self.on_crear_solicitud).grid(row=3, column=0, columnspan=2, pady=10)

    # Eventos que envían datos al controlador
    def on_registrar_cliente(self):
        dni, nombre = self.ent_dni.get(), self.ent_nombre.get()
        if dni and nombre:
            self.controlador.registrar_cliente(dni, nombre)
            self.ent_dni.delete(0, tk.END)
            self.ent_nombre.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Llene todos los campos.")

    def on_crear_solicitud(self):
        dni, monto, plazo = self.ent_sol_dni.get(), self.ent_monto.get(), self.ent_plazo.get()
        try:
            self.controlador.crear_solicitud(dni, float(monto), int(plazo))
            self.ent_monto.delete(0, tk.END)
            self.ent_plazo.delete(0, tk.END)
        except ValueError:
            messagebox.showwarning("Error", "Monto y Plazo deben ser números válidos.")


class TabRiesgos(ttk.Frame):
    """ Módulo para Analistas de Riesgos (HU-03) """
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.crear_widgets()

    def crear_widgets(self):
        ttk.Label(self, text="Solicitudes Pendientes de Aprobación").pack(pady=5)
        
        self.tree = ttk.Treeview(self, columns=("ID", "Cliente", "Monto", "Estado"), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Button(self, text="Aprobar Solicitud Seleccionada", command=self.on_aprobar).pack(pady=10)

    def on_aprobar(self):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion)
            id_sol = item['values'][0]
            self.controlador.procesar_solicitud(id_sol, "Aprobado")
        else:
            messagebox.showwarning("Aviso", "Seleccione una solicitud.")

    def actualizar_tabla(self, solicitudes):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for sol in solicitudes:
            if sol['estado'] == "Pendiente":
                self.tree.insert('', tk.END, values=(sol['id'], sol['nombre_cliente'], sol['monto'], sol['estado']))


class TabOperaciones(ttk.Frame):
    """ Módulo para Operaciones / Desembolsos (HU-04) """
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.crear_widgets()

    def crear_widgets(self):
        ttk.Label(self, text="Solicitudes Listas para Desembolsar").pack(pady=5)
        
        self.tree = ttk.Treeview(self, columns=("ID", "Cliente", "Monto", "Estado"), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Button(self, text="Ejecutar Desembolso", command=self.on_desembolsar).pack(pady=10)

    def on_desembolsar(self):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion)
            id_sol = item['values'][0]
            self.controlador.ejecutar_desembolso(id_sol)
        else:
            messagebox.showwarning("Aviso", "Seleccione una solicitud.")

    def actualizar_tabla(self, solicitudes):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for sol in solicitudes:
            if sol['estado'] == "Aprobado":
                self.tree.insert('', tk.END, values=(sol['id'], sol['nombre_cliente'], sol['monto'], sol['estado']))

class TabConsultas(ttk.Frame):
    """ Módulo para ver la Base de Datos en crudo (Debug) """
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.crear_widgets()

    def crear_widgets(self):
        lbl = ttk.Label(self, text="Base de Datos en Supabase (Estado actual)")
        lbl.pack(pady=5)
        
        self.text_debug = tk.Text(self, height=20, width=80)
        self.text_debug.pack(padx=10, pady=10, fill="both", expand=True)
        
        ttk.Button(self, text="Refrescar Datos", command=self.controlador.refrescar_vistas).pack(pady=5)

    def actualizar_datos(self, clientes, solicitudes, prestamos):
        self.text_debug.delete(1.0, tk.END)
        
        self.text_debug.insert(tk.END, f"--- CLIENTES REGISTRADOS ({len(clientes)}) ---\n")
        for c in clientes:
            self.text_debug.insert(tk.END, f" DNI: {c.get('dni')} | Nombre: {c.get('nombre')} | Registro: {c.get('fecha_registro')}\n")
        
        self.text_debug.insert(tk.END, f"\n--- SOLICITUDES ({len(solicitudes)}) ---\n")
        for sol in solicitudes:
            self.text_debug.insert(tk.END, f" ID: {sol.get('id')} | Estado: {sol.get('estado')} | Monto: {sol.get('monto')} | Cliente: {sol.get('nombre_cliente')}\n")

        self.text_debug.insert(tk.END, f"\n--- PRÉSTAMOS ACTIVOS/DEUDA ({len(prestamos)}) ---\n")
        for p in prestamos:
            self.text_debug.insert(tk.END, f" ID Préstamo: {p.get('id_prestamo')} | DNI: {p.get('dni_cliente')} | Saldo: {p.get('saldo_actual')}\n")