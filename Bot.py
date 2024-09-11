import telebot
import requests

# Токен вашего бота
TOKEN = '6732720595:AAFePTUr9fb4678Avx4Y74ViuSBJQQ8mACM'
bot = telebot.TeleBot(TOKEN)

# Переменная для хранения текущей загадки и ответа
current_riddle = None
current_answer = None

def fetch_riddle():
    # Используем API для получения загадок
    url = 'https://jservice.io/api/random'
    response = requests.get(url)
    data = response.json()
    riddle = data[0]['question']
    answer = data[0]['answer']
    return riddle, answer

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напишите /play, чтобы начать игру в загадки.")

# Обработчик команды /play
@bot.message_handler(commands=['play'])
def start_game(message):
    global current_riddle, current_answer
    current_riddle, current_answer = fetch_riddle()
    bot.reply_to(message, f"Загадка: {current_riddle}")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def check_answer(message):
    global current_riddle, current_answer
    if current_riddle:
        if message.text.strip().lower() == current_answer.lower():
            bot.reply_to(message, "Правильно! Поздравляю!")
            current_riddle = None  # Заканчиваем текущую загадку
            current_answer = None
        else:
            bot.reply_to(message, "Неправильно. Попробуйте еще раз!")
    else:
        bot.reply_to(message, "Напишите /play, чтобы начать игру.")

# Запуск бота
bot.polling()
