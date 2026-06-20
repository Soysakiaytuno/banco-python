from unittest.mock import patch, MagicMock
from modelo import BaseDeDatos

@patch('modelo.create_client')
def test_monto_valido(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    mock_supabase.table().select().eq().execute().data = [{"dni": "12345678", "nombre": "Andres Segoviano"}]
    db = BaseDeDatos()
    exito, mensaje = db.validar_monto(5000)
    assert exito is True
    assert mensaje == "El monto es válido"

@patch('modelo.create_client')
def test_monto_invalido(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    mock_supabase.table().select().eq().execute().data = [{"dni": "12345678", "nombre": "Andres Segoviano"}]
    db = BaseDeDatos()
    exito, mensaje = db.validar_monto(-5000)
    assert exito is False
    assert mensaje == "El monto debe ser mayor a 0"

    
