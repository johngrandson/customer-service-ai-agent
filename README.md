# Atendimento ao Cliente para Clínica Odontológica

Este exemplo demonstra uma configuração multiagente para lidar com diferentes solicitações de atendimento ao cliente em uma clínica odontológica, utilizando o framework Swarm. Os agentes podem triar solicitações, lidar com agendamentos de consultas, fornecer informações sobre convênios e esclarecer dúvidas gerais dos pacientes.

## Agentes

1. **Agente de Triagem**: Determina o tipo de solicitação e transfere para o agente apropriado.
2. **Agente de Agendamento**: Gerencia pedidos de agendamento, confirmação e remarcação de consultas. Solicita informações sobre a data e horário preferidos e verifica a disponibilidade.
3. **Agente de Atendimento Geral**: Responde a perguntas frequentes sobre a clínica, incluindo:
   - Convênios aceitos
   - Tipos de tratamentos oferecidos
   - Horários de funcionamento
   - Opções de pagamento e planos odontológicos

## Configuração

Após instalar as dependências e o Swarm, execute o exemplo com o seguinte comando:

```shell
python3 main.py
