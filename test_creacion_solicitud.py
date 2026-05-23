from unittest.mock import patch, MagicMock
from modelo import BaseDeDatos

@patch('modelo.create_client')
def test_hu02_crear_solicitud_happy_path(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    mock_supabase.table().select().eq().execute().data = [{"dni": "12345678", "nombre": "Juan Perez"}]

    db = BaseDeDatos()
    exito, mensaje = db.crear_solicitud("12345678", 5000, 12)

    assert exito is True
    assert mensaje == "Solicitud guardada en Supabase correctamente."

@patch('modelo.create_client')
def test_hu02_crear_solicitud_unhappy_path(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    mock_supabase.table().select().eq().execute().data = []

    db = BaseDeDatos()
    exito, mensaje = db.crear_solicitud("99999999", 5000, 12)

    assert exito is False
    assert mensaje == "Cliente no encontrado. Regístrelo primero."

@patch('modelo.create_client')
def test_hu01_registrar_cliente_happy_path(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    mock_supabase.table().select().eq().execute().data = []

    db = BaseDeDatos()
    exito, mensaje = db.registrar_cliente("12345678", "Juan Perez")

    assert exito is True
    assert mensaje == "Cliente registrado exitosamente en la nube."
    mock_supabase.table().insert.assert_called_once_with({"dni": "12345678", "nombre": "Juan Perez"})

@patch('modelo.create_client')
def test_hu01_registrar_cliente_unhappy_path(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    mock_supabase.table().select().eq().execute().data = [{"dni": "12345678", "nombre": "Juan Perez"}]

    db = BaseDeDatos()
    exito, mensaje = db.registrar_cliente("12345678", "Juan Perez")

    assert exito is False
    assert mensaje == "El cliente ya existe en la base de datos."