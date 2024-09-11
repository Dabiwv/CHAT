import telebot
from telebot import types
import random

# Токен бота
TOKEN = '6732720595:AAFePTUr9fb4678Avx4Y74ViuSBJQQ8mACM'
bot = telebot.TeleBot(TOKEN)

# Загадки
easy_riddles = [
    {"question": "Что всегда растет, но не живет?", "answer": "Возраст"},
    {"question": "У меня много ключей, но ни одного замка. Что это?", "answer": "Фортепиано"},
    {"question": "Какой день недели идет после пятницы?", "answer": "Суббота"},
    {"question": "Что можно поймать, но нельзя бросить?", "answer": "Холод"},
    {"question": "Какой месяц короче остальных?", "answer": "Февраль"},
    {"question": "Что имеет много зубов, но не кусает?", "answer": "Гребень"},
    {"question": "Какой овощ можно найти в супе?", "answer": "Картошка"},
    {"question": "Какой предмет не имеет начала и конца?", "answer": "Круг"},
    {"question": "Какой овощ всегда идет в паре с другим?", "answer": "Чеснок"},
    {"question": "Что можно держать в одной руке, но не может быть в другой?", "answer": "Собственная рука"}
]

hard_riddles = [
    {"question": "У меня есть тело, но нет головы. У меня есть ноги, но нет рук. Что это?", "answer": "Стол"},
    {"question": "Что уходит из дому утром и возвращается вечером, но не проходит никуда?", "answer": "Тень"},
    {"question": "Что увеличивается, если его перевернуть, и уменьшается, если сложить?", "answer": "Число"},
    {"question": "Какой месяц в году начинается с буквы 'Я'?", "answer": "Январь"},
    {"question": "Какой предмет можно разбить, но он будет жить, а если его не тронуть, то он будет умереть?", "answer": "Сердце"},
    {"question": "Что нельзя сжечь, если положить в огонь?", "answer": "Тень"},
    {"question": "Что не имеет дверей, но можно входить и выходить?", "answer": "Время"},
    {"question": "Что имеет много иголок, но не колет?", "answer": "Елка"},
    {"question": "Что можно взять, но не удержать?", "answer": "Время"},
    {"question": "Что не может быть сдвинуто с места, если это камень?", "answer": "Гора"}
]

# Клавиатура команд
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Легкие загадки")
btn2 = types.KeyboardButton("Сложные загадки")
btn3 = types.KeyboardButton("Команды")
markup.add(btn1, btn2, btn3)

# Хранение текущего состояния пользователя
user_state = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Выберите уровень сложности:", reply_markup=markup)

# Обработчик кнопок
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    
    if message.text == "Легкие загадки":
        user_state[chat_id] = "easy"
        send_riddle(chat_id, easy_riddles)
    
    elif message.text == "Сложные загадки":
        user_state[chat_id] = "hard"
        send_riddle(chat_id, hard_riddles)
    
    elif message.text == "Команды":
        bot.send_message(chat_id, "Доступные команды:\nЛегкие загадки\nСложные загадки\nКоманды")
    
    elif chat_id in user_state:
        state = user_state[chat_id]
        riddles = easy_riddles if state == "easy" else hard_riddles
        
        if message.text.lower() == get_current_riddle_answer(chat_id).lower():
            bot.send_message(chat_id, "Правильно! Загадка решена.")
            send_riddle(chat_id, riddles)
        else:
            bot.send_message(chat_id, "Попробуйте снова.")
    
    else:
        bot.send_message(chat_id, "Выберите команду из меню.")

def send_riddle(chat_id, riddles):
    riddle = random.choice(riddles)
    bot.send_message(chat_id, riddle["question"])
    user_state[chat_id] = {"riddle": riddle["answer"]}

def get_current_riddle_answer(chat_id):
    return user_state[chat_id]["riddle"]

# Запуск бота
bot.polling()
