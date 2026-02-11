import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# --- TRUQUE DE ENGENHARIA ---
# Criamos um 'Ansible Falso' na memória antes mesmo de importar o script.
# Isso evita erros de 'ModuleNotFoundError' ou crashes do AnsibleModule.
mock_ansible = MagicMock()
sys.modules['ansible'] = mock_ansible
sys.modules['ansible.module_utils'] = mock_ansible
sys.modules['ansible.module_utils.basic'] = mock_ansible
# ----------------------------

# Adiciona a raiz ao Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora importamos o módulo (que vai usar o Ansible falso)
from library.modbus_check import request_modbus

@patch('socket.create_connection')
def test_read_success(mock_create_connection):
    mock_sock = MagicMock()
    # Simula resposta: Header + Data (10, 20)
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
