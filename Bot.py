from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Запуск браузера
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Открыть WhatsApp Web
driver.get("https://web.whatsapp.com")

# Ожидание сканирования QR-кода
input("После сканирования QR-кода нажмите Enter")

def send_message(contact_name, message):
    # Поиск контакта
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.send_keys(contact_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    # Поиск поля для ввода сообщения и отправка сообщения
    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="6"]')
    message_box.send_keys(message)
    message_box.send_keys(Keys.RETURN)

# Пример использования
send_message("Контакт", "Привет, это автоматическое сообщение!")

# Закрытие браузера
time.sleep(5)
driver.quit()
