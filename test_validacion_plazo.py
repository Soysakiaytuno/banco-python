from unittest.mock import patch, MagicMock
from modelo import BaseDeDatos

@patch('modelo.create_client')
def test_plazo_valido(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    db = BaseDeDatos()
    exito, mensaje = db.validar_plazo(12)
    assert exito is True
    assert mensaje == "El plazo es válido"

@patch('modelo.create_client')
def test_plazo_invalido(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    db = BaseDeDatos()
    exito, mensaje = db.validar_plazo(0)
    assert exito is False
    assert mensaje == "El plazo debe ser mayor a 0"
