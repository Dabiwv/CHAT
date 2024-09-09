import telebot
from telebot import types

# Токен бота
TOKEN = '6692785864:AAEqASjDj-9JcmIZKGOjCSgvXWXDv7E7KaY'
bot = telebot.TeleBot(TOKEN)

# Вопросы для последовательного прохождения
questions = [
    "Ты один?",
    "Ты без мамы?",
    "Ты без отца?",
    "Ты без совести, готов убить пса?",
    "Любишь негров?",
    "Ты расист?",
    "Ты одобряешь нацизм?",
    "Любишь казахов?",
    "А узбеков?",
    "Ну может палочку сникерса?"
]

# Последнее сообщение, если все вопросы пройдены
final_message = "МОЛОДЕЦ. Ты олицетворение изгоя. Твой шанс на отца 5%"

# Словарь для отслеживания текущего вопроса каждого пользователя
user_progress = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_progress[user_id] = 0  # Начинаем с первого вопроса
    ask_question(user_id)

# Функция для отправки вопроса пользователю
def ask_question(user_id):
    question_index = user_progress.get(user_id, 0)
    
    # Если вопросы закончились, отправляем финальное сообщение
    if question_index >= len(questions):
        bot.send_message(user_id, final_message)
        return
    
    # Создаем кнопки Да и Нет
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    yes_button = types.KeyboardButton("Да")
    no_button = types.KeyboardButton("Нет")
    markup.add(yes_button, no_button)
    
    # Отправляем текущий вопрос
    bot.send_message(user_id, questions[question_index], reply_markup=markup)

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.from_user.id
    
    # Увеличиваем индекс вопроса для пользователя
    if user_id in user_progress:
        user_progress[user_id] += 1
    
    # Переходим к следующему вопросу
    ask_question(user_id)

# Запуск бота
bot.polling()
