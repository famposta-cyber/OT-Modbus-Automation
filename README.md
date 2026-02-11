# OT Modbus Automation Framework

Automação para ambientes industriais críticos (OT) utilizando Ansible e Python.

## Estrutura
- `library/`: Módulo customizado Modbus TCP.
- `playbooks/`: Rotinas de verificação e telemetria.
- `tests/`: Testes unitários para validação de lógica.

## Execução Rápida
```bash
ansible-playbook -i inventory/hosts.ini playbooks/site.yml