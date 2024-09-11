import telebot
import sympy as sp

# Токен вашего бота
TOKEN = '6732720595:AAFePTUr9fb4678Avx4Y74ViuSBJQQ8mACM'
bot = telebot.TeleBot(TOKEN)

# Основная функция для обработки математических выражений
@bot.message_handler(func=lambda message: True)
def handle_math(message):
    try:
        math_expression = message.text.strip()

        # Проверяем, есть ли переменные, чтобы решать уравнения
        if '=' in math_expression:
            left_side, right_side = math_expression.split('=')
            # Создаем переменную 'x' для решения уравнений
            x = sp.Symbol('x')
            equation = sp.Eq(sp.sympify(left_side), sp.sympify(right_side))
            solution = sp.solve(equation, x)
            bot.send_message(message.chat.id, f'Решение уравнения: {solution}')
        else:
            # Вычисляем обычные выражения
            result = sp.sympify(math_expression)
            bot.send_message(message.chat.id, f'Ответ: {result}')

    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка в выражении: {e}')

# Запуск бота
bot.polling()
