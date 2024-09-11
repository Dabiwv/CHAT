import telebot
import random
from telebot import types

TOKEN = '6732720595:AAFePTUr9fb4678Avx4Y74ViuSBJQQ8mACM'
bot = telebot.TeleBot(TOKEN)

# Начальный баланс для каждого игрока
starting_balance = 2500

# Словарь для хранения балансов пользователей
balances = {}

# Функция для генерации выигрыша с шансом на проигрыш
def spin_result(amount):
    win_chance = random.uniform(0, 100)  # Генерируем шанс выигрыша
    if win_chance <= 50:  # 50% шанс на проигрыш
        return -amount  # Проигрыш
    else:
        multiplier = random.uniform(1.2, 1.5)  # Множитель выигрыша от 1.2 до 1.5
        return amount * multiplier - amount  # Чистый выигрыш

# Функция для получения шанса на выигрыш
def calculate_chance():
    return round(random.uniform(10, 100), 2)  # Шанс от 10% до 100%

# Команда /start - приветствие и установка начального баланса
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    balances[user_id] = starting_balance
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    commands_button = types.KeyboardButton("Команды")
    markup.add(commands_button)
    bot.send_message(message.chat.id, f"Привет! Ваш начальный баланс: {starting_balance} 💰", reply_markup=markup)

# Команда для отображения текущего баланса
@bot.message_handler(commands=['balance'])
def balance(message):
    user_id = message.from_user.id
    balance = balances.get(user_id, starting_balance)
    bot.send_message(message.chat.id, f"Ваш текущий баланс: {balance:.2f} 💰")

# Команда /spin для ставок в слоте
@bot.message_handler(commands=['spin'])
def spin(message):
    try:
        user_id = message.from_user.id
        balance = balances.get(user_id, starting_balance)

        # Получаем сумму ставки
        amount = int(message.text.split()[1])

        # Проверяем, что ставка больше или равна 25
        if amount < 25:
            bot.send_message(message.chat.id, "Минимальная ставка 25 💰")
            return

        # Проверяем, что у пользователя достаточно средств
        if amount > balance:
            bot.send_message(message.chat.id, "Недостаточно средств на балансе.")
            return

        # Генерируем результат ставки
        result = spin_result(amount)
        balance += result
        balances[user_id] = balance

        if result > 0:
            bot.send_message(message.chat.id, f"Поздравляем! Вы выиграли {result:.2f} 💰!")
        else:
            bot.send_message(message.chat.id, f"К сожалению, вы проиграли {abs(result):.2f} 💰.")

        bot.send_message(message.chat.id, f"Ваш новый баланс: {balance:.2f} 💰")

    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Пожалуйста, используйте формат команды: /spin [сумма]")

# Команда /casino - аналогичная /spin
@bot.message_handler(commands=['casino'])
def casino(message):
    try:
        user_id = message.from_user.id
        balance = balances.get(user_id, starting_balance)

        # Получаем сумму ставки
        amount = int(message.text.split()[1])

        # Проверяем минимальную ставку
        if amount < 25:
            bot.send_message(message.chat.id, "Минимальная ставка 25 💰")
            return

        # Проверяем баланс
        if amount > balance:
            bot.send_message(message.chat.id, "Недостаточно средств на балансе.")
            return

        # Генерируем результат
        result = spin_result(amount)
        balance += result
        balances[user_id] = balance

        if result > 0:
            bot.send_message(message.chat.id, f"Поздравляем! Вы выиграли {result:.2f} 💰 в Казино!")
        else:
            bot.send_message(message.chat.id, f"К сожалению, вы проиграли {abs(result):.2f} 💰.")

        bot.send_message(message.chat.id, f"Ваш новый баланс: {balance:.2f} 💰")

    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Пожалуйста, используйте формат команды: /casino [сумма]")

# Команда /lottery для лотереи
@bot.message_handler(commands=['lottery'])
def lottery(message):
    try:
        user_id = message.from_user.id
        balance = balances.get(user_id, starting_balance)

        # Получаем сумму ставки
        amount = int(message.text.split()[1])

        # Проверяем минимальную ставку
        if amount < 25:
            bot.send_message(message.chat.id, "Минимальная ставка 25 💰")
            return

        # Проверяем баланс
        if amount > balance:
            bot.send_message(message.chat.id, "Недостаточно средств на балансе.")
            return

        # Генерируем результат лотереи
        result = spin_result(amount)
        balance += result
        balances[user_id] = balance

        if result > 0:
            bot.send_message(message.chat.id, f"Поздравляем! Вы выиграли {result:.2f} 💰 в Лотерее!")
        else:
            bot.send_message(message.chat.id, f"К сожалению, вы проиграли {abs(result):.2f} 💰.")

        bot.send_message(message.chat.id, f"Ваш новый баланс: {balance:.2f} 💰")

    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Пожалуйста, используйте формат команды: /lottery [сумма]")

# Команда /chance для отображения шансов на выигрыш
@bot.message_handler(commands=['chance'])
def chance(message):
    try:
        user_id = message.from_user.id
        amount = int(message.text.split()[1])

        # Генерация шанса
        chance = calculate_chance()

        bot.send_message(message.chat.id, f"Ваш шанс на выигрыш составляет {chance}%")

    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Пожалуйста, используйте формат команды: /chance [сумма]")

# Кнопка "Команды" для отображения всех доступных команд
@bot.message_handler(func=lambda message: message.text == "Команды")
def show_commands(message):
    commands = """
/start - Начать игру
/balance - Проверить баланс
/spin [сумма] - Сделать ставку в слоте
/casino [сумма] - Сделать ставку в казино
/lottery [сумма] - Сделать ставку в лотерее
/chance [сумма] - Узнать шанс на выигрыш
"""
    bot.send_message(message.chat.id, commands)

# Запуск бота
bot.polling()
