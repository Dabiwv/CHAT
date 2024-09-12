import telebot
from telebot import types
import time
import re

# Токен бота
TOKEN = '7058388588:AAHWd-c2BEmG8penT2VXGxveMg-tftPeJWs'
bot = telebot.TeleBot(TOKEN)

# Меню команд
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("📸 Взломать Instagram")
btn2 = types.KeyboardButton("🖼 Взломать VK")
btn3 = types.KeyboardButton("📧 Взломать Google")
markup.add(btn1, btn2, btn3)

# Хранение данных пользователя
user_data = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "HACK CRACK TOOL:\n"
                                      "Выберите цель взлома:", reply_markup=markup)

# Обработка выбора "взломать Instagram", VK, Google
@bot.message_handler(func=lambda message: message.text in ["📸 Взломать Instagram", "🖼 Взломать VK", "📧 Взломать Google"])
def ask_account_info(message):
    bot.send_message(message.chat.id, "Пожалуйста, введите следующие данные:\n"
                                      "1) Никнейм\n"
                                      "2) Ссылку\n"
                                      "3) Фотографию профиля.")
    bot.register_next_step_handler(message, validate_data)

# Проверка введенных данных
def validate_data(message):
    # Проверка формата никнейма
    lines = message.text.split('\n')
    
    if len(lines) < 2:
        bot.send_message(message.chat.id, "Ошибка: Необходимо ввести как минимум Никнейм и ссылку.")
        return
    
    nickname = lines[0]
    link = lines[1]

    # Проверка ссылки (простая проверка на наличие 'http' или 'https')
    if not re.match(r'http[s]?://', link):
        bot.send_message(message.chat.id, "Ошибка: Неправильный формат ссылки.")
        return
    
    # Если данные валидны, начать имитацию взлома
    user_data[message.chat.id] = {"nickname": nickname, "link": link}
    bot.send_message(message.chat.id, "Отлично! Начинаем процесс взлома. Это займет некоторое время.")
    time.sleep(5)  # Небольшая задержка перед процессом
    simulate_hack(message)

# Имитация взлома с этапами
def simulate_hack(message):
    bot.send_message(message.chat.id, "⚙️ Проверка данных...")
    time.sleep(10)
    bot.send_message(message.chat.id, "🔑 Попытка взлома пароля...")
    time.sleep(10)
    bot.send_message(message.chat.id, "💾 Декодирование данных аккаунта...")
    time.sleep(10)
    bot.send_message(message.chat.id, "⏳ Завершаем процесс взлома...")
    time.sleep(15)
    
    # Завершение имитации
    nickname = user_data[message.chat.id]["nickname"]
    bot.send_message(message.chat.id, f"✅ Взлом завершен! Вот ваши данные:\n"
                                      f"Логин: {nickname}\n"
                                      f"Пароль: hack_me_12345")

# Запуск бота
bot.polling(none_stop=True)
