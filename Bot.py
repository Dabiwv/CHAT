import telebot
from telebot import types
import random

# Токен бота
TOKEN = '6732720595:AAFePTUr9fb4678Avx4Y74ViuSBJQQ8mACM'
bot = telebot.TeleBot(TOKEN)

# Клавиатура команд
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Угадай число")
btn2 = types.KeyboardButton("Камень, ножницы, бумага")
btn3 = types.KeyboardButton("Слот-машина")
btn4 = types.KeyboardButton("Команды")
markup.add(btn1, btn2, btn3, btn4)

# Хранение текущего состояния пользователя
user_state = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Выбери игру:", reply_markup=markup)

# Обработчик кнопок
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    if message.text == "Угадай число":
        user_state[chat_id] = "guess_number"
        bot.send_message(chat_id, "Я загадал число от 1 до 10. Попробуй угадать!")

    elif message.text == "Камень, ножницы, бумага":
        user_state[chat_id] = "rps"
        bot.send_message(chat_id, "Выбери: Камень, Ножницы или Бумага", reply_markup=create_rps_markup())

    elif message.text == "Слот-машина":
        user_state[chat_id] = "slot_machine"
        result = spin_slot_machine()
        bot.send_message(chat_id, result)

    elif message.text == "Команды":
        bot.send_message(chat_id, "Доступные команды:\nУгадай число\nКамень, ножницы, бумага\nСлот-машина\nКоманды")

    elif chat_id in user_state:
        if user_state[chat_id] == "guess_number":
            handle_guess_number(chat_id, message.text)
        elif user_state[chat_id] == "rps":
            handle_rps(chat_id, message.text)
        else:
            bot.send_message(chat_id, "Выбери команду из меню.")

# Угадай число
def handle_guess_number(chat_id, guess):
    try:
        number = int(guess)
        correct_number = random.randint(1, 10)
        if number == correct_number:
            bot.send_message(chat_id, f"Правильно! Я загадал {correct_number}.")
        else:
            bot.send_message(chat_id, f"Неправильно! Я загадал {correct_number}.")
        user_state.pop(chat_id)
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введи число от 1 до 10.")

# Камень, ножницы, бумага
def create_rps_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Камень"), types.KeyboardButton("Ножницы"), types.KeyboardButton("Бумага"))
    return markup

def handle_rps(chat_id, user_choice):
    choices = ["Камень", "Ножницы", "Бумага"]
    bot_choice = random.choice(choices)
    result = ""

    if user_choice == bot_choice:
        result = f"Ничья! Я выбрал {bot_choice}."
    elif (user_choice == "Камень" and bot_choice == "Ножницы") or \
         (user_choice == "Ножницы" and bot_choice == "Бумага") or \
         (user_choice == "Бумага" and bot_choice == "Камень"):
        result = f"Ты выиграл! Я выбрал {bot_choice}."
    else:
        result = f"Ты проиграл! Я выбрал {bot_choice}."

    bot.send_message(chat_id, result)
    user_state.pop(chat_id)

# Слот-машина
def spin_slot_machine():
    symbols = ["🍒", "🍋", "🔔", "💎", "7️⃣"]
    slots = [random.choice(symbols) for _ in range(3)]
    result = " | ".join(slots)

    if len(set(slots)) == 1:
        return f"{result}\nПоздравляем! Ты выиграл!"
    else:
        return f"{result}\nПопробуй снова!"

# Запуск бота
bot.polling()
