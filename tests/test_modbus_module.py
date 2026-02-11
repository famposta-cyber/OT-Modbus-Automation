import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Adiciona o diretório library ao path para importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../library')))
from modbus_check import request_modbus

@patch('socket.create_connection')
def test_read_success(mock_create_connection):
    # Mock do Socket para simular resposta de sucesso [10, 20]
    mock_sock = MagicMock()
    # Header(7) + FC(1) + ByteCount(1) + Data(4 bytes = 2 words)
    # Data: 00 0A (10), 00 14 (20)
    mock_sock.recv.return_value = b'\x00\x01\x00\x00\x00\x06\x01\x03\x04\x00\x0A\x00\x14'
    mock_create_connection.return_value.__enter__.return_value = mock_sock

    success, data = request_modbus('127.0.0.1', 502, 1, 0, 2, 1)
    
    assert success is True
    assert data == [10, 20]

@patch('socket.create_connection')
def test_connection_error(mock_create_connection):
    mock_create_connection.side_effect = Exception("Connection refused")
    
    success, data = request_modbus('127.0.0.1', 502, 1, 0, 1, 1)
    
    assert success is False
    assert "Connection refused" in data