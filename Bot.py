from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токен бота
TOKEN = '6692785864:AAEqASjDj-9JcmIZKGOjCSgvXWXDv7E7KaY'

# Вопросы для бота
questions = [
    "Ты один?",
    "Ты без мамы?",
    "Ты без отца?",
    "Ты без совести готов убить пса?",
    "Любишь негров?",
    "Ты расист?",
    "Ты одобряешь нацизм?",
    "Любишь казахов?",
    "А узбеков?",
    "Ну может палочку сникерса?"
]

# Последнее сообщение вместо вопроса
final_message = "МОЛОДЕЦ. Ты олицетворение изгоя. Твой шанс на отца 5%"

# Словарь для отслеживания прогресса пользователей
user_progress = {}

# Стартовая команда
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_progress[user_id] = 0  # Начинаем с первого вопроса
    ask_question(update, context, user_id)

# Функция для отправки вопроса
def ask_question(update: Update, context: CallbackContext, user_id):
    # Получаем текущий индекс вопроса пользователя
    question_index = user_progress.get(user_id, 0)
    
    # Если вопросы закончились, отправляем финальное сообщение
    if question_index >= len(questions):
        update.message.reply_text(final_message)
        del user_progress[user_id]  # Удаляем прогресс пользователя
        return
    
    # Отправляем текущий вопрос
    question = questions[question_index]
    
    # Кнопки Да и Нет
    reply_markup = ReplyKeyboardMarkup([['Да', 'Нет']], one_time_keyboard=True, resize_keyboard=True)
    context.bot.send_message(chat_id=user_id, text=question, reply_markup=reply_markup)

# Функция обработки ответа пользователя
def handle_response(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    
    # Проверяем, есть ли пользователь в списке тех, кто проходит опрос
    if user_id in user_progress:
        # Увеличиваем индекс вопроса на 1
        user_progress[user_id] += 1
        ask_question(update, context, user_id)
    else:
        # Если пользователь не начал опрос, просим его начать с команды /start
        update.message.reply_text("Пожалуйста, начните с команды /start.")

# Обработчики команд и сообщений
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

# Команда /start
dispatcher.add_handler(CommandHandler('start', start))

# Обработчик сообщений с ответами
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_response))

# Запуск бота
updater.start_polling()
updater.idle()
