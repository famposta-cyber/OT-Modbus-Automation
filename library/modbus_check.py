#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import struct
import sys

# Tenta importar Ansible, se falhar (teste local), segue sem ele.
try:
    from ansible.module_utils.basic import AnsibleModule
except ImportError:
    AnsibleModule = None

def request_modbus(host, port, unit_id, address, count, timeout):
    try:
        transaction_id = 1
        protocol_id = 0
        length = 6
        header = struct.pack('>HHHB', transaction_id, protocol_id, length, unit_id)
        payload = struct.pack('>BHH', 0x03, address, count)
        
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.send(header + payload)
            response = sock.recv(1024)
            if len(response) < 9: return False, "Resposta incompleta"
            if response[7] & 0x80: return False, "Modbus Exception: " + str(response[8])
            byte_count = response[8]
            data = response[9:9+byte_count]
            registers = list(struct.unpack(f'>{byte_count//2}H', data))
            return True, registers
    except Exception as e:
        return False, str(e)

def run_module():
    module_args = dict(host=dict(type='str', required=True), port=dict(type='int', default=502), unit_id=dict(type='int', default=1), address=dict(type='int', required=True), count=dict(type='int', default=1), timeout=dict(type='int', default=5))
    if AnsibleModule is None: sys.exit(1)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    success, result = request_modbus(module.params['host'], module.params['port'], module.params['unit_id'], module.params['address'], module.params['count'], module.params['timeout'])
    if success: module.exit_json(changed=False, registers=result)
    else: module.fail_json(msg=result)

if __name__ == '__main__':
    run_module()