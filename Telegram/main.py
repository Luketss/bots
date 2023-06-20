import telebot

API_TOKEN = "SEU_TOKEN"

CHAT_ID = "SEU_CHAT_ID"

bot = telebot.TeleBot(API_TOKEN)

bot.send_message(
    CHAT_ID, text="O bot do vídeo está em execução, digite /start para chamar"
)


@bot.message_handler(commands=["start"])
def enviar_ola(message):
    bot.reply_to(message, "Olá, bem vindo!")


bot.infinity_polling()
