from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
import time
import json

# Настройка браузера
browser = uc.Chrome()
browser.get('https://www.ozon.ru/')
time.sleep(3)

try:
    # Поиск и ввод запроса
    search_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Искать на Ozon']"))
    )
    search_input.send_keys("шуруповерт зубр")
    search_input.submit()
    time.sleep(5)

    # Прокрутка страницы для загрузки всех товаров
    for _ in range(2):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Собираем все карточки товаров
    product_cards = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.j8r_25"))
    )
    print(f"Найдено карточек товаров: {len(product_cards)}")
except Exception as e:
    print(f'Ошибка {e}')