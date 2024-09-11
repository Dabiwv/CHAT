import telebot
import random

TOKEN = '6732720595:AAFePTUr9fb4678Avx4Y74ViuSBJQQ8mACM'
bot = telebot.TeleBot(TOKEN)

# Начальный баланс
starting_balance = 2500

# Джекпот
jackpot = 1000

# Словарь для хранения балансов пользователей
balances = {}

# Функция для генерации выигрыша с множителем
def generate_win(amount):
    global jackpot
    chance = random.uniform(0, 1)  # Вероятность от 0 до 1

    if chance <= 0.5:  # 50% шанс проигрыша
        jackpot += amount * 0.05  # 5% проигрыша добавляются в джекпот
        return 0, chance * 100
    elif chance <= 0.8:  # 30% шанс маленького выигрыша
        win_amount = amount * 1.5  # Выигрыш в 1.5 раза больше
        return win_amount, chance * 100
    elif chance <= 0.95:  # 15% шанс среднего выигрыша
        win_amount = amount * 2  # Выигрыш в 2 раза больше
        return win_amount, chance * 100
    else:  # 5% шанс сорвать джекпот
        win_amount = jackpot
        jackpot = 1000  # Обновляем джекпот после выигрыша
        return win_amount, chance * 100

# Команда "старт"
@bot.message_handler(commands=['start'])
def start(message):
    balances[message.from_user.id] = starting_balance
    bot.send_message(message.chat.id, "Добро пожаловать в игру! Ваш начальный баланс: {} 💰".format(starting_balance))

# Команда "баланс"
@bot.message_handler(commands=['balance'])
def balance(message):
    balance = balances.get(message.from_user.id, starting_balance)
    bot.send_message(message.chat.id, "Ваш текущий баланс: {} 💰".format(balance))

# Команда "спин"
@bot.message_handler(commands=['spin'])
def spin(message):
    try:
        amount = int(message.text.split()[1])
        if amount < 25:
            bot.send_message(message.chat.id, "Минимальная ставка 25 💰")
            return
        
        balance = balances.get(message.from_user.id, starting_balance)
        if amount > balance:
            bot.send_message(message.chat.id, "Недостаточно средств для ставки.")
            return
        
        win_amount, chance = generate_win(amount)
        balance -= amount
        balance += win_amount
        balances[message.from_user.id] = balance
        
        if win_amount == 0:
            bot.send_message(message.chat.id, "К сожалению, вы проиграли. Шанс выигрыша: {:.2f}%".format(chance))
        else:
            bot.send_message(message.chat.id, "Поздравляем! Вы выиграли {:.2f} 💰 (Шанс выигрыша: {:.2f}%)".format(win_amount, chance))
        
        bot.send_message(message.chat.id, "Ваш текущий баланс: {} 💰".format(balance))
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Используйте команду /spin [сумма]")

# Команда "шанс"
@bot.message_handler(commands=['chance'])
def chance(message):
    try:
        amount = int(message.text.split()[1])
        if amount < 25:
            bot.send_message(message.chat.id, "Минимальная ставка 25 💰")
            return

        chance = random.uniform(10, 100)
        bot.send_message(message.chat.id, "Ваш шанс на выигрыш составляет {:.2f}%".format(chance))
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Используйте команду /chance [сумма]")

# Кнопка "команды"
@bot.message_handler(commands=['commands'])
def commands(message):
    bot.send_message(message.chat.id, "/spin [сумма] - Сделать ставку в слоте\n"
                                      "/balance - Узнать ваш баланс\n"
                                      "/chance [сумма] - Узнать шанс выигрыша")

# Запуск бота
bot.polling()
