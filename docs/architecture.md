# Arquitetura da Solução

O fluxo de automação segue o modelo "Controller-Agentless":

1. **Ansible Controller:** Executa os playbooks.
2. **Modbus Module:** Conecta via TCP (Porta 502) aos PLCs.
3. **Inventory:** Define a topologia das plantas (Vitória, Itabira).

## Diagrama de Fluxo
[Ansible] --(TCP/502)--> [Switch OT] --> [PLC 01]
                                     --> [PLC 02]