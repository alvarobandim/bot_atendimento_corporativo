# Helpdesk NOC Bot

Uma solução de backend desenvolvida em Python para automatizar a triagem e notificação de incidentes de TI via Telegram. O objetivo deste projeto é otimizar o fluxo de atendimento, reduzindo o tempo de resposta da equipe de suporte (NOC - Network Operations Center).

## Como funciona (Under the hood)

O bot opera em duas frentes simultâneas:
1. **B2C (Interface com o Usuário):** Funciona como uma URA (Menu de Autoatendimento), onde o usuário interage, relata o problema e recebe um protocolo de atendimento.
2. **B2B (Integração com a Equipe):** Assim que o ticket é gerado, o sistema persiste os dados localmente e faz o roteamento ativo, enviando um Push Notification (Alerta) direto para o grupo privado da equipe de TI.

## Stack Tecnológica

- **Linguagem:** Python 3
- **Integrações:** Telegram Bot API (`pyTelegramBotAPI`)
- **Arquitetura:** Polling assíncrono, Manipulação de I/O (Persistência de logs), FSM (Finite State Machine) para controle de steps da conversa.

## Como rodar o projeto localmente

1. Faça o clone do repositório:
   ```bash
   git clone [https://github.com/seu_usuario/bot_atendimento_corporativo.git](https://github.com/seu_usuario/bot_atendimento_corporativo.git)