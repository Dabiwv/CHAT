import telebot
from telebot import types

# Инициализация бота с токеном
TOKEN = '6692785864:AAEqASjDj-9JcmIZKGOjCSgvXWXDv7E7KaY'
ADMIN_ID = 1694921116
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения данных пользователей
user_data = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    name_button = types.KeyboardButton("Начать сбор данных")
    markup.add(name_button)
    bot.send_message(user_id, "Привет! Нажмите 'Начать сбор данных', чтобы предоставить информацию.", reply_markup=markup)

# Обработчик кнопки "Начать сбор данных"
@bot.message_handler(func=lambda message: message.text == "Начать сбор данных")
def ask_name(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Пожалуйста, введите ваше имя:")
    bot.register_next_step_handler(message, process_name)

def process_name(message):
    user_id = message.from_user.id
    user_data[user_id] = {'name': message.text}
    bot.send_message(user_id, "Пожалуйста, введите вашу фамилию:")
    bot.register_next_step_handler(message, process_surname)

def process_surname(message):
    user_id = message.from_user.id
    user_data[user_id]['surname'] = message.text
    bot.send_message(user_id, "Пожалуйста, введите ваш возраст:")
    bot.register_next_step_handler(message, process_age)

def process_age(message):
    user_id = message.from_user.id
    try:
        user_data[user_id]['age'] = int(message.text)
        bot.send_message(user_id, "Пожалуйста, введите ваш номер телефона:")
        bot.register_next_step_handler(message, process_phone)
    except ValueError:
        bot.send_message(user_id, "Пожалуйста, введите корректный возраст.")

def process_phone(message):
    user_id = message.from_user.id
    user_data[user_id]['phone'] = message.text
    # Отправка данных администратору
    admin_message = (
        f"Новый пользователь:\n"
        f"Имя: {user_data[user_id]['name']}\n"
        f"Фамилия: {user_data[user_id]['surname']}\n"
        f"Возраст: {user_data[user_id]['age']}\n"
        f"Телефон: {user_data[user_id]['phone']}\n"
    )
    bot.send_message(ADMIN_ID, admin_message)
    bot.send_message(user_id, "Спасибо! Ваши данные были отправлены.")

# Запуск бота
bot.polling()
