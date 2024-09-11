import telebot
import time

TOKEN = '6732720595:AAFePTUr9fb4678Avx4Y74ViuSBJQQ8mACM'
bot = telebot.TeleBot(TOKEN)

# Состояние пользователя для отслеживания ответа
user_state = {}

# Полная таблица умножения с примерами
multiplication_questions = [
    ("2x2=", 4), ("2x3=", 6), ("2x4=", 8), ("2x5=", 10), ("2x6=", 12), ("2x7=", 14), ("2x8=", 16), ("2x9=", 18),
    ("3x2=", 6), ("3x3=", 9), ("3x4=", 12), ("3x5=", 15), ("3x6=", 18), ("3x7=", 21), ("3x8=", 24), ("3x9=", 27),
    ("4x2=", 8), ("4x3=", 12), ("4x4=", 16), ("4x5=", 20), ("4x6=", 24), ("4x7=", 28), ("4x8=", 32), ("4x9=", 36),
    ("5x2=", 10), ("5x3=", 15), ("5x4=", 20), ("5x5=", 25), ("5x6=", 30), ("5x7=", 35), ("5x8=", 40), ("5x9=", 45),
    ("6x2=", 12), ("6x3=", 18), ("6x4=", 24), ("6x5=", 30), ("6x6=", 36), ("6x7=", 42), ("6x8=", 48), ("6x9=", 54),
    ("7x2=", 14), ("7x3=", 21), ("7x4=", 28), ("7x5=", 35), ("7x6=", 42), ("7x7=", 49), ("7x8=", 56), ("7x9=", 63),
    ("8x2=", 16), ("8x3=", 24), ("8x4=", 32), ("8x5=", 40), ("8x6=", 48), ("8x7=", 56), ("8x8=", 64), ("8x9=", 72),
    ("9x2=", 18), ("9x3=", 27), ("9x4=", 36), ("9x5=", 45), ("9x6=", 54), ("9x7=", 63), ("9x8=", 72), ("9x9=", 81)
]

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Ты готов изучать умножение, додик?")
    user_state[message.chat.id] = 'waiting_for_response'

# Обработчик ответов
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    if user_state.get(chat_id) == 'waiting_for_response':
        if message.text.lower() == 'да':
            # Начинаем с первого примера
            bot.send_message(chat_id, multiplication_questions[0][0])
            user_state[chat_id] = {'progress': 0}
        elif message.text.lower() == 'нет':
            send_annoying_messages(chat_id)
        else:
            bot.send_message(chat_id, "Ответь 'да' или 'нет', додик!")

    elif isinstance(user_state.get(chat_id), dict):  # Проверяем ответ на вопрос
        try:
            answer = int(message.text)
            current_question_index = user_state[chat_id]['progress']
            correct_answer = multiplication_questions[current_question_index][1]

            if answer == correct_answer:
                bot.send_message(chat_id, "Правильно!")
                user_state[chat_id]['progress'] += 1
                next_question_index = user_state[chat_id]['progress']

                if next_question_index < len(multiplication_questions):
                    bot.send_message(chat_id, multiplication_questions[next_question_index][0])
                else:
                    bot.send_message(chat_id, "Ты прошел всю таблицу умножения! Поздравляю, додик!")
                    user_state.pop(chat_id)  # Сброс состояния
            else:
                bot.send_message(chat_id, "Неправильно, попробуй снова!")
        except ValueError:
            bot.send_message(chat_id, "Введи число, а не текст, додик!")

# Функция для надоедливых сообщений, если пользователь сказал 'нет'
def send_annoying_messages(chat_id):
    for _ in range(120):
        bot.send_message(chat_id, "Ты ничего не добьёшься!")
        time.sleep(0.2)  # Задержка между сообщениями

# Запуск бота
bot.polling()
