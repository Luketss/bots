import asyncio
from telebot.async_telebot import AsyncTeleBot

import MetaTrader5 as mt5
from setup import token, login, senha

API_TOKEN = token

bot = AsyncTeleBot(API_TOKEN)

order_types = {
    "/comprar": mt5.ORDER_TYPE_BUY,
    "/vender": mt5.ORDER_TYPE_SELL,
}


@bot.message_handler(commands=["teste"])
async def send_welcome(message):
    text = "Oi eu sou o seu robô.\nTa tudo funcionando!"
    await bot.reply_to(message, text)


@bot.message_handler(commands=["comprar", "vender"])
async def send_welcome(message):
    print(message.text)
    ord_type, symbol, lot = message.text.split(" ")
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        await bot.reply_to(message, "Ticker da ação não existe")

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            await bot.reply_to(message, f"Ticker não foi adicionado ao mt5 {symbol}")

    price = mt5.symbol_info_tick(symbol).ask
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(lot),
        "type": order_types.get(ord_type),
        "price": price,
        "magic": 234000,
        "comment": "python script",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    # send a trading request
    result = mt5.order_send(request)
    print(result)
    await bot.reply_to(message, result)


if __name__ == "__main__":
    try:
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            quit()
        mt5.login(login, senha, server="XPMT5-DEMO")
        asyncio.run(bot.polling())
    finally:
        mt5.shutdown()
