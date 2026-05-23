from unittest.mock import patch, MagicMock
from modelo import BaseDeDatos

@patch('modelo.create_client')
def test_hu04_desembolsar_prestamo_happy_path(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    mock_supabase.table().select().eq().execute().data = [{"id": 99, "estado": "Aprobado", "dni_cliente": "12345667", "monto": 5000}]
    db = BaseDeDatos()
    exito, mensaje = db.desembolsar_prestamo(99)
    assert exito is True
    assert mensaje == "Desembolso exitoso. Préstamo generado en la base de datos."
    mock_supabase.table().update.assert_called_once_with({"estado": "Desembolsado"})
    mock_supabase.table().insert.assert_called_once_with({"id_solicitud": 99, "dni_cliente": "12345667", "saldo_actual": 5000})
