import json
import time
import requests
import telebot


class TelegramBot:
    token = "seu_token"

    def __init__(self):
        self.bot_id_messages = list()
        self.bot = telebot.TeleBot(self.token)
        print("Bot inicializado")

    def enviar_mensagem(self, chat_id, text):
        message = self.bot.send_message(chat_id=chat_id, text=text)
        if message != None:
            print("Mensagem enviada com sucesso")
        self.bot_id_messages.append(message)

    def deletar_mensagem(self, chat_id, message_id):
        is_deleted = self.bot.delete_message(chat_id=chat_id, message_id=message_id)
        if is_deleted:
            print("Mensagem excluída com sucesso")


class Blaze:
    def __init__(self, url="https://blaze1.space"):
        self.url = url
        self.tl = TelegramBot()

    def buscar_dados_recentes(self):
        recent_url = f"{self.url}/api/roulette_games/recent"
        resposta = requests.get(recent_url)
        json_resposta = json.loads(resposta.text)
        return json_resposta

    def checar_padrao(self, resultados):
        lista_reversa = resultados[::-1]
        contador_vermelhos = 0
        for index, value in enumerate(lista_reversa):
            if index < 5 and value.get("color") == 1:
                contador_vermelhos += 1
        return contador_vermelhos

    def play(self):
        chaves_para_manter = ["id", "color", "roll"]
        r = self.buscar_dados_recentes()
        resultados = []

        for d in r:
            new_dict = {chave: d[chave] for chave in chaves_para_manter if chave in d}
            resultados.append(new_dict)
        while True:
            r = self.buscar_dados_recentes()
            for value in r:
                id = value.get("id")
                if list(filter(lambda item: item["id"] == id, resultados)):
                    pass
                else:
                    resultados.append(
                        {
                            chave: value[chave]
                            for chave in chaves_para_manter
                            if chave in value
                        }
                    )
                    padrao = self.checar_padrao(resultados)
                    print(padrao)
                    if padrao == 5:
                        self.tl.enviar_mensagem("chat id", "entrada confirmada")
            time.sleep(15)
            print(resultados)


if __name__ == "__main__":
    # tl = TelegramBot()
    # tl.enviar_mensagem("-123456", "test")
    # tl.deletar_mensagem("-123456", "1")
    obj = Blaze()
    obj.play()
