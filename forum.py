from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import os

import config


def forum_req(name):
    driver_path = 'C:/Users/админ/PycharmProjects/HelperSCbot/chromedriver-win32/chromedriver.exe'
    output_file = f'message_{name}.txt'  # Имя файла для хранения последнего сообщения
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск в фоновом режиме (без графического интерфейса)
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f'https://forum.exbo.net/u/{name}')

    # Установка куки
    cookies = config.cooki

    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(10)  # Ждем загрузки страницы
    try:
        first_post_body = driver.find_element("class name", "Post-body")
        new_message = first_post_body.text

        # Извлечение ссылки на сообщение
        link_element = driver.find_element("css selector", ".PostsUserPage-discussion a")
        message_link = link_element.get_attribute('href') if link_element else None

        if os.path.exists(f'history_message/{output_file}'):
            with open(f'history_message/{output_file}', 'r', encoding='utf-8') as file:
                last_message = file.read().strip()
        else:
            last_message = ""

        if new_message == last_message:
            print("Изменений нет.")
            return None
        else:
            with open(f'history_message/{output_file}', 'w', encoding='utf-8') as file:
                file.write(new_message)

            print("Новое сообщение:", new_message)
            print("Ссылка на сообщение:", message_link)  # Выводим ссылку на сообщение
            return new_message, message_link  # Возвращаем и сообщение, и ссылку
    except Exception as ex:
        print('[ORANGE ERROR] forum_req error', ex)


def forum_mes(nameS):
    if isinstance(nameS, str):
        return forum_req(nameS)
    elif isinstance(nameS, list):
        messages = []
        for name in nameS:
            message = forum_req(name)
            if message:
                messages.append(message)
        return messages
    else:
        print(f'[MIDL ERROR] {nameS} не имеет класс str или list')
        return False