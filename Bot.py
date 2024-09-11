import telebot
from telebot import types
import random

# Токен бота
TOKEN = '6732720595:AAFePTUr9fb4678Avx4Y74ViuSBJQQ8mACM'
bot = telebot.TeleBot(TOKEN)

# Начальный баланс
INITIAL_BALANCE = 2500

# Словарь для хранения балансов пользователей
user_balances = {}

# Функция для генерации случайного выигрыша
def generate_win(amount):
    win_chance = random.uniform(0.1, 1)  # Шанс выигрыша от 10% до 100%
    win_amount = amount * win_chance
    return win_amount, win_chance * 100

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = INITIAL_BALANCE
    bot.send_message(user_id, "Добро пожаловать в казино! Ваш баланс: 2500 💰")
    show_commands(message)

# Функция для отображения доступных команд
def show_commands(message):
    markup = types.InlineKeyboardMarkup()
    btn_commands = types.InlineKeyboardButton("Команды", callback_data="show_commands")
    markup.add(btn_commands)
    bot.send_message(message.from_user.id, "Нажмите кнопку ниже для получения списка команд.", reply_markup=markup)

# Обработчик нажатия на кнопку "Команды"
@bot.callback_query_handler(func=lambda call: call.data == "show_commands")
def handle_commands(call):
    commands = (
        "/start - Начать игру\n"
        "/spin <сумма> - Играть в слот\n"
        "/balance - Проверить баланс\n"
        "/chance <сумма> - Проверить шанс на выигрыш\n"
        "/casino <сумма> - Казино\n"
        "/lottery <сумма> - Лотерея"
    )
    bot.send_message(call.message.chat.id, f"Доступные команды:\n{commands}")

# Обработчик команды /spin
@bot.message_handler(commands=['spin'])
def spin_command(message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        bot.send_message(user_id, "Для начала игры используйте команду /start")
        return
    
    try:
        amount = int(message.text.split()[1])
        if amount < 25:
            bot.send_message(user_id, "Минимальная ставка: 25 💰")
            return
        
        if amount > user_balances[user_id]:
            bot.send_message(user_id, "Недостаточно средств!")
            return
        
        win_amount, win_chance = generate_win(amount)
        user_balances[user_id] -= amount
        if win_amount > 0:
            user_balances[user_id] += win_amount
            result_message = f"Поздравляем! Вы выиграли {win_amount:.2f} 💰 (Шанс выигрыша: {win_chance:.2f}%)"
        else:
            result_message = "К сожалению, вы проиграли. Попробуйте снова!"
        
        bot.send_message(user_id, result_message)
        bot.send_message(user_id, f"Ваш текущий баланс: {user_balances[user_id]:.2f} 💰")
        
    except IndexError:
        bot.send_message(user_id, "Укажите сумму ставки: /spin <сумма>")
    except ValueError:
        bot.send_message(user_id, "Сумма ставки должна быть числом.")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Ошибка Telegram API: {e}")

# Обработчик команды /balance
@bot.message_handler(commands=['balance'])
def balance_command(message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        bot.send_message(user_id, "Для начала игры используйте команду /start")
        return
    
    bot.send_message(user_id, f"Ваш текущий баланс: {user_balances[user_id]:.2f} 💰")

# Обработчик команды /chance
@bot.message_handler(commands=['chance'])
def chance_command(message):
    try:
        amount = int(message.text.split()[1])
        if amount < 25:
            bot.send_message(message.chat.id, "Минимальная ставка: 25 💰")
            return
        
        chance = random.uniform(10, 100)  # Шанс от 10% до 100%
        bot.send_message(message.chat.id, f"Ваш шанс на выигрыш составляет {chance:.2f}%")
    
    except IndexError:
        bot.send_message(message.chat.id, "Укажите сумму ставки: /chance <сумма>")
    except ValueError:
        bot.send_message(message.chat.id, "Сумма ставки должна быть числом.")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Ошибка Telegram API: {e}")

# Обработчик команды /casino
@bot.message_handler(commands=['casino'])
def casino_command(message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        bot.send_message(user_id, "Для начала игры используйте команду /start")
        return
    
    try:
        amount = int(message.text.split()[1])
        if amount < 25:
            bot.send_message(user_id, "Минимальная ставка: 25 💰")
            return
        
        if amount > user_balances[user_id]:
            bot.send_message(user_id, "Недостаточно средств!")
            return
        
        win_amount, win_chance = generate_win(amount)
        user_balances[user_id] -= amount
        if win_amount > 0:
            user_balances[user_id] += win_amount
            result_message = f"Поздравляем! Вы выиграли {win_amount:.2f} 💰 (Шанс выигрыша: {win_chance:.2f}%)"
        else:
            result_message = "К сожалению, вы проиграли. Попробуйте снова!"
        
        bot.send_message(user_id, result_message)
        bot.send_message(user_id, f"Ваш текущий баланс: {user_balances[user_id]:.2f} 💰")
        
    except IndexError:
        bot.send_message(user_id, "Укажите сумму ставки: /casino <сумма>")
    except ValueError:
        bot.send_message(user_id, "Сумма ставки должна быть числом.")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Ошибка Telegram API: {e}")

# Обработчик команды /lottery
@bot.message_handler(commands=['lottery'])
def lottery_command(message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        bot.send_message(user_id, "Для начала игры используйте команду /start")
        return
    
    try:
        amount = int(message.text.split()[1])
        if amount < 25:
            bot.send_message(user_id, "Минимальная ставка: 25 💰")
            return
        
        if amount > user_balances[user_id]:
            bot.send_message(user_id, "Недостаточно средств!")
            return
        
        win_amount, win_chance = generate_win(amount)
        user_balances[user_id] -= amount
        if win_amount > 0:
            user_balances[user_id] += win_amount
            result_message = f"Поздравляем! Вы выиграли {win_amount:.2f} 💰 (Шанс выигрыша: {win_chance:.2f}%)"
        else:
            result_message = "К сожалению, вы проиграли. Попробуйте снова!"
        
        bot.send_message(user_id, result_message)
        bot.send_message(user_id, f"Ваш текущий баланс: {user_balances[user_id]:.2f} 💰")
        
    except IndexError:
        bot.send_message(user_id, "Укажите сумму ставки: /lottery <сумма>")
    except ValueError:
        bot.send_message(user_id, "Сумма ставки должна быть числом.")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Ошибка Telegram API: {e}")

# Запуск бота
bot.polling()
