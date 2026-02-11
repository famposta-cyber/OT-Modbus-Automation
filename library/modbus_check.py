#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import socket
import struct

DOCUMENTATION = r'''
---
module: modbus_check
short_description: Leitura de registradores Modbus TCP
description:
  - Conecta via socket puro para ler Holding Registers (FC03) de PLCs e Gateways.
options:
  host:
    description: IP ou Hostname do alvo.
    required: true
    type: str
  port:
    description: Porta TCP Modbus.
    default: 502
    type: int
  unit_id:
    description: ID da Unidade (Slave ID).
    default: 1
    type: int
  address:
    description: Endereço do registrador inicial.
    required: true
    type: int
  count:
    description: Quantidade de registradores a ler.
    default: 1
    type: int
  timeout:
    description: Timeout do socket em segundos.
    default: 5
    type: int
'''

def request_modbus(host, port, unit_id, address, count, timeout):
    transaction_id = 1
    protocol_id = 0
    length = 6 
    
    header = struct.pack('>HHHB', transaction_id, protocol_id, length, unit_id)
    payload = struct.pack('>BHH', 0x03, address, count)
    
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.send(header + payload)
            response = sock.recv(1024)
            
            if len(response) < 9:
                return False, "Resposta incompleta"
            
            if response[7] & 0x80:
                return False, f"Modbus Exception: {response[8]}"
            
            byte_count = response[8]
            data = response[9:9+byte_count]
            # Desempacota lista de unsigned short (2 bytes)
            registers = list(struct.unpack(f'>{byte_count//2}H', data))
            return True, registers
    except Exception as e:
        return False, str(e)

def run_module():
    module_args = dict(
        host=dict(type='str', required=True),
        port=dict(type='int', default=502),
        unit_id=dict(type='int', default=1),
        address=dict(type='int', required=True),
        count=dict(type='int', default=1),
        timeout=dict(type='int', default=5)
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    
    success, result = request_modbus(
        module.params['host'], module.params['port'],
        module.params['unit_id'], module.params['address'],
        module.params['count'], module.params['timeout']
    )

    if success:
        module.exit_json(changed=False, registers=result)
    else:
        module.fail_json(msg=result)

if __name__ == '__main__':
    run_module()