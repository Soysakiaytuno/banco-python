from unittest.mock import patch, MagicMock
from modelo import BaseDeDatos

@patch('modelo.create_client')
def test_validar_dni_existente(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    mock_supabase.table().select().eq().execute().data = [{"dni": "12345678", "nombre": "Andres Segoviano"}]
    db = BaseDeDatos()
    exito, mensaje = db.validar_cliente("12345678")
    assert exito is True
    assert mensaje == "Cliente registrado correctamente."

@patch('modelo.create_client')
def test_validar_dni_no_existe(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    mock_supabase.table().select().eq().execute().data = []
    db = BaseDeDatos()
    exito, mensaje = db.validar_cliente("12345678973738989polo")
    assert exito is False
    assert mensaje == "El DNI no se encuentra registrado."
    