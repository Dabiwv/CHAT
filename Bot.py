import telebot
import language_tool_python

# Токен вашего бота
TOKEN = '6732720595:AAFePTUr9fb4678Avx4Y74ViuSBJQQ8mACM'
bot = telebot.TeleBot(TOKEN)

# Инициализация инструмента для проверки орфографии (по умолчанию русский)
tool = language_tool_python.LanguageTool('ru')  # Указание русского языка для проверки

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def check_spelling(message):
    text = message.text
    # Поиск ошибок в предложении
    matches = tool.check(text)
    
    if not matches:
        bot.send_message(message.chat.id, "Ошибок не найдено!")
    else:
        # Исправляем ошибки
        corrected_text = language_tool_python.utils.correct(text, matches)
        bot.send_message(message.chat.id, f'Исправлено:\n{corrected_text}')

# Запуск бота
bot.polling()
