from unittest.mock import patch
from modelo import BaseDeDatos

@patch('modelo.validar_cliente')
def test_validar_dni_existente(mock_supabase):
    db = BaseDeDatos()
    exito, mensaje = db.validar_cliente("12345678")
    assert exito is True
    assert mensaje == "Cliente registrado correctamente."

@patch('modelo.validar_cliente')
def test_validar_dni_no_existe(mock_supabase):
    db = BaseDeDatos()
    exito, mensaje = db.validar_cliente("12345678973738989polo")
    assert exito is False
    assert mensaje == "El DNI no se encuentra registrado."
    