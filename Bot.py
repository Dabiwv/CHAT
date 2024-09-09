from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from telegram.ext import CallbackQueryHandler
from telegram import ParseMode

# Замените на ваш токен
API_TOKEN = '6692785864:AAEqASjDj-9JcmIZKGOjCSgvXWXDv7E7KaY'

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Отправьте ваш номер телефона.')

def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    text = update.message.text
    
    # Если сообщение похоже на номер телефона, выводим его
    if text.isdigit() and len(text) >= 10:
        print(f'Получен номер телефона от пользователя {user_id}: {text}')
        update.message.reply_text(f'Ваш номер телефона: {text} успешно получен!')
    else:
        update.message.reply_text('Пожалуйста, отправьте действительный номер телефона.')

def main():
    updater = Updater(token=API_TOKEN, use_context=True)
    
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
