import time
import json
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests


def login_to_blaze(driver, login="", senha=""):
    isCaptcha = True
    driver.get("https://blaze-4.com/pt/")
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='unauthed-buttons']//div[1]")
        )
    )
    driver.find_element(By.XPATH, "//div[@class='unauthed-buttons']//div[1]").click()
    time.sleep(2)
    login_box = driver.find_element(By.XPATH, "//input[@name='username']")
    login_box.send_keys(login)
    senha_box = driver.find_element(By.XPATH, "(//input[@name='password'])[1]")
    senha_box.send_keys(senha)
    time.sleep(1)
    driver.find_element(By.XPATH, "(//button[normalize-space()='Entrar'])[1]").click()
    while isCaptcha:
        a = input("Resolva o captcha e digite 1 quando estiver pronto: ")
        if a == "1":
            isCaptcha = False
    time.sleep(3)


def goto_double_page(driver) -> None:
    driver.get("https://blaze.com/pt/games/double")


def get_current_time_hours():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def today_date():
    today = datetime.today()

    yesterday = today - timedelta(days=1)

    print(today.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d"))
    return (today.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d"))


def estrategia(result_array):
    color_count = 0
    last = None
    for color in result_array:
        if last == None:
            last = color
        if color == last:
            color_count += 1

        else:
            return color_count
    return color_count


def get_last_result_double():
    """
    Precisa ser chamada dentro da pagina da Blaze
    """
    today, yesterday = today_date()
    cur_time = get_current_time_hours()
    results = []
    try:
        r = requests.get(
            f"https://blaze.com/api/roulette_games/history?startDate={yesterday}T{cur_time}.000Z&endDate={today}T{cur_time}.000Z&page=1"
        )
        data = json.loads(r.text)

        for i, v in enumerate(data["records"]):
            val = v["color"]
            if i < 5:
                results.append(val)
        if estrategia(results) < 0:
            return True
        return False
    except ValueError as e:
        print(e)


def make_bet(driver):
    """
    Função não criada
    """
    quantia = driver.find_element(By.XPATH, "//input[@type='number']")
    quantia.send_keys("4")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    login_to_blaze(driver, "seu_email", "sua_senha")
    goto_double_page(driver)
    while True:
        if get_last_result_double():
            print("Hora de fazer entrada")
            driver.quit()
            break
        print("Entrada não atingida")
        time.sleep(5)
