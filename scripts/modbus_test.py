import socket
import struct
import sys

def quick_check(ip, address):
    """Script rápido para rodar direto no shell sem Ansible"""
    try:
        s = socket.create_connection((ip, 502), timeout=2)
        # Monta pacote hardcoded para leitura simples
        req = struct.pack('>HHHBBHH', 1, 0, 6, 1, 3, address, 1)
        s.send(req)
        res = s.recv(1024)
        s.close()
        
        if res:
            val = struct.unpack('>H', res[9:11])[0]
            print(f"[OK] {ip} Addr {address} = {val}")
        else:
            print(f"[ERR] {ip} Sem resposta")
    except Exception as e:
        print(f"[FAIL] {ip}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 modbus_test.py <IP> <ADDR>")
    else:
        quick_check(sys.argv[1], int(sys.argv[2]))