import MetaTrader5 as mt5
from setup import user, senha


if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()


autorizado = mt5.login(user, senha, server="XPMT5-DEMO")
print(autorizado)
