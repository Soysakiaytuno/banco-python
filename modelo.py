import os
from supabase import create_client, Client

SUPABASE_URL = "https://ujykhkyfdguebnniujyd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVqeWtoa3lmZGd1ZWJubml1anlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE2MzUwMzUsImV4cCI6MjA4NzIxMTAzNX0.c6PGflPhGW6xDDtRIKQhlQ9B_so7nu3XEg-awbww9Fo"

class BaseDeDatos:
    def __init__(self):
        # Inicializamos la conexión a Supabase
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def registrar_cliente(self, dni, nombre):
        try:
            # 1. Verificamos si el DNI ya existe
            respuesta = self.supabase.table('clientes').select('*').eq('dni', dni).execute()
            if len(respuesta.data) > 0:
                return False, "El cliente ya existe en la base de datos."
            
            # 2. Insertamos el nuevo cliente
            self.supabase.table('clientes').insert({"dni": dni, "nombre": nombre}).execute()
            return True, "Cliente registrado exitosamente en la nube."
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"

    def crear_solicitud(self, dni, monto, plazo):
        try:
            # 1. Verificamos que el cliente exista
            cliente = self.supabase.table('clientes').select('*').eq('dni', dni).execute()
            if len(cliente.data) == 0:
                return False, "Cliente no encontrado. Regístrelo primero."
            
            # 2. Insertamos la solicitud (el ID y la fecha se generan solos en Supabase)
            self.supabase.table('solicitudes').insert({
                "dni_cliente": dni,
                "monto": monto,
                "plazo": plazo,
                "estado": "Pendiente"
            }).execute()
            return True, "Solicitud guardada en Supabase correctamente."
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"

    def actualizar_estado_solicitud(self, id_solicitud, nuevo_estado):
        try:
            # Actualizamos solo el campo estado
            self.supabase.table('solicitudes').update({"estado": nuevo_estado}).eq('id', id_solicitud).execute()
            return True
        except Exception as e:
            print(f"Error actualizando estado: {e}")
            return False

    def desembolsar_prestamo(self, id_solicitud):
        try:
            # 1. Obtener los detalles de la solicitud
            sol = self.supabase.table('solicitudes').select('*').eq('id', id_solicitud).execute()
            
            if len(sol.data) == 0 or sol.data[0]['estado'] != 'Aprobado':
                return False, "Solicitud no válida o no ha sido aprobada."
            
            solicitud = sol.data[0]

            # 2. Actualizar estado de la solicitud a 'Desembolsado'
            self.supabase.table('solicitudes').update({"estado": "Desembolsado"}).eq('id', id_solicitud).execute()

            # 3. Crear el préstamo (la deuda activa del cliente)
            self.supabase.table('prestamos').insert({
                "id_solicitud": solicitud['id'],
                "dni_cliente": solicitud['dni_cliente'],
                "saldo_actual": solicitud['monto']
            }).execute()

            return True, "Desembolso exitoso. Préstamo generado en la base de datos."
        except Exception as e:
            return False, f"Error en BD: {str(e)}"

    def obtener_solicitudes(self):
        """
        Esta función consulta todas las solicitudes y hace un 'JOIN' con la tabla 
        clientes para traernos también el nombre del cliente.
        """
        try:
            # Consultamos las solicitudes e incluimos el nombre desde la tabla relacionada 'clientes'
            respuesta = self.supabase.table('solicitudes').select('id, monto, estado, dni_cliente, clientes(nombre)').execute()
            
            # Formateamos los datos para que las Vistas de Tkinter los entiendan igual que antes
            solicitudes_formateadas = []
            for fila in respuesta.data:
                nombre_cliente = fila['clientes']['nombre'] if fila.get('clientes') else 'Desconocido'
                
                solicitudes_formateadas.append({
                    'id': fila['id'],
                    'dni_cliente': fila['dni_cliente'],
                    'nombre_cliente': nombre_cliente,
                    'monto': fila['monto'],
                    'estado': fila['estado']
                })
            
            # Ordenamos por ID para que las más antiguas salgan primero
            solicitudes_formateadas.sort(key=lambda x: x['id'])
            return solicitudes_formateadas
            
        except Exception as e:
            print(f"Error al obtener solicitudes: {e}")
            return []

    def obtener_clientes(self):
        """Consulta todos los clientes registrados en Supabase."""
        try:
            respuesta = self.supabase.table('clientes').select('*').execute()
            return respuesta.data
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
            return []

    def obtener_prestamos(self):
        """Consulta todos los préstamos activos en Supabase."""
        try:
            respuesta = self.supabase.table('prestamos').select('*').execute()
            return respuesta.data
        except Exception as e:
            print(f"Error al obtener préstamos: {e}")
            return []