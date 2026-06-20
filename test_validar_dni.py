from unittest.mock import patch, MagicMock
from modelo import BaseDeDatos

@patch('modelo.validar_cliente')
def test_validar_dni_existente(mock_validar_cliente):
    mock_supabase = MagicMock()
    mock_validar_cliente.return_value = mock_supabase
    mock_supabase.table().select().eq().execute().data = [{"dni": "12345678", "nombre": "Andres Segoviano"}]
    db = BaseDeDatos()
    exito, mensaje = db.validar_cliente("12345678")
    assert exito is True
    assert mensaje == "Cliente registrado correctamente."

@patch('modelo.validar_cliente')
def test_validar_dni_no_existe(mock_validar_cliente):
    mock_supabase = MagicMock()
    mock_validar_cliente.return_value = mock_supabase
    mock_supabase.table().select().eq().execute().data = []
    db = BaseDeDatos()
    exito, mensaje = db.validar_cliente("12345678973738989polo")
    assert exito is False
    assert mensaje == "El DNI no se encuentra registrado."
    