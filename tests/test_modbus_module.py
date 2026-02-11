import sys
import os
from unittest.mock import MagicMock, patch

# Adiciona a raiz do projeto ao Path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library.modbus_check import request_modbus


# Teste 1: Leitura de sucesso (Nota: 2 linhas em branco acima deste comentário)
@patch('socket.create_connection')
def test_read_success(mock_create_connection):
    mock_sock = MagicMock()
    mock_sock.recv.return_value = b'\x00\x01\x00\x00\x00\x06\x01\x03\x04\x00\x0A\x00\x14'
    mock_create_connection.return_value.__enter__.return_value = mock_sock

    success, data = request_modbus('127.0.0.1', 502, 1, 0, 2, 1)

    assert success is True
    assert data == [10, 20]


# Teste 2: Erro de conexão (Nota: 2 linhas em branco acima deste comentário)
@patch('socket.create_connection')
def test_connection_error(mock_create_connection):
    mock_create_connection.side_effect = Exception("Connection refused")

    success, data = request_modbus('127.0.0.1', 502, 1, 0, 1, 1)

    assert success is False
    assert "Connection refused" in str(data)