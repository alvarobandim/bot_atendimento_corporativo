import telebot
import random
from datetime import datetime

# --- Configs & Credentials (Atenção: Usar .env em ambiente de Produção) ---
TOKEN = "COLE_O_SEU_TOKEN_DO_BOTFATHER_AQUI"
ID_GRUPO_TI = "COLE_O_ID_DO_GRUPO_AQUI"

bot = telebot.TeleBot(TOKEN)
print("[INFO] Serviço de Bot NOC inicializado.")

# --- Handlers / Entrypoints ---

@bot.message_handler(commands=["start", "ajuda"])
def cmd_start(mensagem):
    """Entrypoint do bot: exibe menu principal de atendimento."""
    menu = (
        "Olá! Sou o Assistente Virtual de TI. 🤖\n\n"
        "Selecione uma opção:\n"
        "[1] 📝 Abrir um Novo Chamado\n"
        "[2] 📞 Falar com um Atendente"
    )
    bot.reply_to(mensagem, menu)


# --- Middlewares de Roteamento ---

@bot.message_handler(func=lambda m: True)
def roteador_opcoes(mensagem):
    """Router simples para validar a opção do usuário e direcionar o fluxo."""
    opcao = mensagem.text
    
    if opcao == "1":
        msg = bot.reply_to(mensagem, "Certo! Qual o problema que está ocorrendo? (ex: Meu monitor não liga)")
        # Registra callback para capturar o payload da próxima interação do usuário
        bot.register_next_step_handler(msg, processar_abertura_chamado)
        
    elif opcao == "2":
        bot.reply_to(mensagem, "Transferindo para a fila de atendimento humano... Aguarde.")
        
    else:
        bot.reply_to(mensagem, "Opção inválida. Digite /start para ver o menu.")


# --- Controllers / Regra de Negócio ---

def processar_abertura_chamado(mensagem):
    """Processa o input do usuário, gera protocolo, persiste o log e dispara push notification pro NOC."""
    payload_problema = mensagem.text
    user_name = mensagem.from_user.first_name
    
    protocolo = random.randint(10000, 99999)
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # 1. Feedback via interface do usuário (Privado)
    feedback = (
        f"✅ Chamado aberto com sucesso!\n\n"
        f"🎫 Protocolo: #{protocolo}\n"
        f"A equipe de infraestrutura já foi notificada."
    )
    bot.reply_to(mensagem, feedback)
    
    # 2. Persistência de Dados (I/O)
    # TODO: Refatorar futuramente para integrar com banco relacional (ex: PostgreSQL)
    with open("chamados_ti.txt", "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] PROT: {protocolo} | USER: {user_name} | ISSUE: {payload_problema}\n")

    # 3. Notificação Ativa para a equipe de suporte (Sala de Guerra / NOC)
    alerta_noc = (
        f"🚨 **NOVO INCIDENTE REGISTRADO** 🚨\n\n"
        f"👤 User: {user_name}\n"
        f"📝 Payload: {payload_problema}\n"
        f"🎫 Prot: #{protocolo}\n"
        f"⏰ TS: {timestamp}"
    )
    bot.send_message(ID_GRUPO_TI, alerta_noc, parse_mode="Markdown")
    print(f"[LOG] Chamado #{protocolo} persistido e notificado ao grupo de suporte.")


# --- Worker / Execução ---
print("[INFO] Bot em modo de escuta (Long Polling)...")
bot.polling()