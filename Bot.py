from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import logging
import json

# Включение логирования для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Замените на ваш API токен
API_TOKEN = '6692785864:AAEqASjDj-9JcmIZKGOjCSgvXWXDv7E7KaY'

# Файл для хранения данных пользователей
DATA_FILE = 'user_data.json'

# Загрузка данных пользователей
def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Сохранение данных пользователей
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    data = load_data()

    # Добавление нового пользователя в данные
    if str(user.id) not in data:
        data[str(user.id)] = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        save_data(data)

    # Создание клавиатуры с кнопкой для запроса номера телефона
    keyboard = [
        [InlineKeyboardButton("Информация о пользователе", callback_data='user_info')],
        [InlineKeyboardButton("Добавить данные", callback_data='add_data')],
        [InlineKeyboardButton("Удалить данные", callback_data='delete_data')],
        [InlineKeyboardButton("Отправить номер телефона", callback_data='request_phone')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Добро пожаловать! Выберите действие из меню ниже:', reply_markup=reply_markup)

# Функция для обработки команды /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Команды:\n/start - Начать использование бота\n/help - Помощь')

# Функция для обработки нажатий на кнопки
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    user_id = str(query.from_user.id)
    data = load_data()

    if query.data == 'user_info':
        user_data = data.get(user_id, {})
        message = (
            f"Информация о пользователе:\n"
            f"Имя: {user_data.get('first_name', 'Не указано')}\n"
            f"Фамилия: {user_data.get('last_name', 'Не указано')}\n"
            f"Юзернейм: {user_data.get('username', 'Не указано')}\n"
        )
        query.edit_message_text(text=message)

    elif query.data == 'add_data':
        query.edit_message_text(text="Введите данные для добавления:")
        return  # Ожидаем ввода от пользователя

    elif query.data == 'delete_data':
        if user_id in data:
            del data[user_id]
            save_data(data)
            query.edit_message_text(text="Данные удалены.")
        else:
            query.edit_message_text(text="Данные не найдены.")
    
    elif query.data == 'request_phone':
        # Запрос номера телефона
        keyboard = [[KeyboardButton("Отправить свой номер", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        query.edit_message_text(text="Пожалуйста, отправьте свой номер телефона:", reply_markup=reply_markup)

# Функция для обработки текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    data = load_data()

    if user_id in data:
        # Обработка ввода пользователя для добавления данных
        user_data = data[user_id]
        user_data['additional_info'] = update.message.text
        save_data(data)
        update.message.reply_text(f"Данные '{update.message.text}' добавлены.")
    else:
        update.message.reply_text('Пожалуйста, используйте команду /start для регистрации.')

# Функция для обработки номера телефона
def handle_contact(update: Update, context: CallbackContext) -> None:
    phone_number = update.message.contact.phone_number
    user_id = update.message.from_user.id

    # Отображение номера телефона в Termux
    logging.info(f"Номер телефона пользователя {user_id}: {phone_number}")

    update.message.reply_text(f"Ваш номер телефона был получен: {phone_number}")

# Основная функция для запуска бота
def main() -> None:
    # Создание объекта Updater и получение диспетчера для регистрации обработчиков
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрация обработчиков команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # Регистрация обработчиков сообщений и кнопок
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.contact, handle_contact))
    dp.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
