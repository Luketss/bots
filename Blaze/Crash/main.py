import time

from selenium import webdriver
from selenium.webdriver.common.by import By


valores_passados = []

driver = webdriver.Chrome()
driver.get("https://blaze-4.com/pt/games/crash")

time.sleep(4)

previous = driver.find_element(By.XPATH, "//div[@class='crash-previous']")

p = previous.find_element(By.XPATH, "//div[@class='entries']")

values = p.find_elements(By.TAG_NAME, "span")

for v in values:
    if v.text != "":
        valores_passados.append(v.text)

print(valores_passados[::-1])

driver.quit()
