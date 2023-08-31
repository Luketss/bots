API_TOKEN = "SEU_TOKEN"
CHAT_ID = "ID DO SEU CHAT/GRUPO"
URL = "https://blaze.com/api/crash_games/recent"

import json
import requests
import telebot

bot = telebot.TeleBot(API_TOKEN)


def blaze():
    resposta = requests.get(URL)
    return resposta.text


def telegram(texto):
    bot.send_message(CHAT_ID, texto)


def pegar_resultado(resposta):
    lista_resultados = []
    json_valores = json.loads(resposta)
    for index, valor in enumerate(json_valores):
        if index < 4:
            if float(valor["crash_point"]) >= 2.0:
                lista_resultados.append(valor["crash_point"])
                print("bom", valor["crash_point"])
            else:
                print("ruim", valor["crash_point"])
    return lista_resultados


if __name__ == "__main__":
    resposta = blaze()
    lista_resultados = pegar_resultado(resposta)
    if len(lista_resultados) > 1:
        telegram("Entrada no jogo crash")
