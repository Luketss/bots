import time

from setup import user, senha

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

valor_aposta = "1"
valor_auto_retirar = "2.5"


def fazer_login():
    login_path = "//input[@name='username']"
    pass_path = "//input[@name='password']"

    browser_lib.find_element(By.XPATH, login_path).send_keys(user)
    browser_lib.find_element(By.XPATH, pass_path).send_keys(senha)

    logar_btn_path = "//button[normalize-space()='Entrar']"
    browser_lib.find_element(By.XPATH, logar_btn_path).click()

    time.sleep(6)


def inserir_aposta():
    quantia_path = "//input[@type='number']"
    quantia_element = browser_lib.find_element(By.XPATH, quantia_path)
    quantia_element.send_keys(valor_aposta)
    auto_retirar_path = "//input[@data-testid='auto-cashout']"
    auto_retirar_element = browser_lib.find_element(By.XPATH, auto_retirar_path)
    auto_retirar_element.clear()
    auto_retirar_element.send_keys(valor_auto_retirar)
    comecar_jogo_btn_path = "//button[normalize-space()='Começar o jogo']"
    browser_lib.find_element(By.XPATH, comecar_jogo_btn_path).click()


def pegar_ultimos_valores():
    div_ultimos_valores_path = "//div[@class='entries']"
    div_valores = browser_lib.find_element(By.XPATH, div_ultimos_valores_path)

    spans = div_valores.find_elements(By.TAG_NAME, "span")

    valores = [v.text for v in spans]
    return spans, valores


def validar_estrategia(spans):
    p1, p2, p3 = (
        spans[0].get_attribute("class"),
        spans[1].get_attribute("class"),
        spans[2].get_attribute("class"),
    )
    print(f"{p1} - {spans[0].text}, {p2} - {spans[1].text}, {p3} - {spans[2].text}")

    if p1 == p2:
        return True
    return False

    # if p1 == p2 and p2 == p3:
    #     return True
    # return False


def main():
    fazer_login()
    while True:
        spans, valores = pegar_ultimos_valores()
        if validar_estrategia(spans):
            inserir_aposta()
            break
        time.sleep(0.5)
    input()


if __name__ == "__main__":
    browser_lib = webdriver.Chrome()
    browser_lib.get("https://blaze-4.com/pt/games/crash?modal=auth&tab=login")
    main()
    browser_lib.close()
