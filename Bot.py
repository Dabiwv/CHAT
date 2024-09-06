import telebot
from telebot import types

# Вставьте свой токен
API_TOKEN = '6692785864:AAEqASjDj-9JcmIZKGOjCSgvXWXDv7E7KaY'
bot = telebot.TeleBot(API_TOKEN)

# Данные об аккаунтах, виртах и кейсах
accounts = {
    'Нуб 6 лвл': {'price': 500, 'description': 'Нет дома, начальное авто'},
    'Средний 10 лвл': {'price': 1500, 'description': 'Есть дом, стандартное авто'},
    'Про 15 лвл': {'price': 3500, 'description': 'Дом в центре, хорошее авто'},
    'Миллиардер 23 лвл': {'price': 10000, 'description': 'Вилла, крутая машина, бизнес'},
}

cases = {
    'Кейс Бомжа': 140,
    'Ежедневный кейс': 200,
    'Стандартный кейс': 350,
    'Особый кейс': 500,
    'Кейс за Блек Коины': 700,
}

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Аккаунты')
    btn2 = types.KeyboardButton('Вирты')
    btn3 = types.KeyboardButton('Кейсы')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Добро пожаловать в магазин! Выберите категорию:", reply_markup=markup)

# Обработка кнопки Аккаунты
@bot.message_handler(lambda message: message.text == 'Аккаунты')
def send_accounts(message):
    markup = types.InlineKeyboardMarkup()
    for account_name in accounts:
        markup.add(types.InlineKeyboardButton(text=account_name, callback_data=f"account_{account_name}"))
    bot.send_message(message.chat.id, "Доступные аккаунты:", reply_markup=markup)

# Обработка выбора аккаунта
@bot.callback_query_handler(func=lambda call: call.data.startswith('account_'))
def account_details(call):
    account_name = call.data.split('account_')[1]
    account_info = accounts[account_name]
    text = f"Аккаунт: {account_name}\nЦена: {account_info['price']} руб.\nОписание: {account_info['description']}"
    payment_methods = types.InlineKeyboardMarkup()
    payment_methods.add(types.InlineKeyboardButton(text="Телеграм кошелек", url="https://t.me/wallet/"))
    payment_methods.add(types.InlineKeyboardButton(text="Kaspi банк", callback_data="kaspi_payment"))
    payment_methods.add(types.InlineKeyboardButton(text="СБП", callback_data="sbp_payment"))
    bot.send_message(call.message.chat.id, text)
    bot.send_message(call.message.chat.id, "Выберите метод оплаты:", reply_markup=payment_methods)

# Обработка кнопки Вирты
@bot.message_handler(lambda message: message.text == 'Вирты')
def send_virts_prompt(message):
    bot.send_message(message.chat.id, "Введите количество виртов (от 50 тыс до 45 млн):")

# Обработка текста с количеством виртов
@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_virts(message):
    virts_amount = int(message.text)
    if 50000 <= virts_amount <= 45000000:
        price = virts_amount * 0.001  # Примерная цена за вирты
        text = f"Вы выбрали {virts_amount} виртов за {price} руб."
        payment_methods = types.InlineKeyboardMarkup()
        payment_methods.add(types.InlineKeyboardButton(text="Телеграм кошелек", url="https://t.me/wallet/"))
        payment_methods.add(types.InlineKeyboardButton(text="Kaspi банк", callback_data="kaspi_payment"))
        payment_methods.add(types.InlineKeyboardButton(text="СБП", callback_data="sbp_payment"))
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "Выберите метод оплаты:", reply_markup=payment_methods)
    else:
        bot.send_message(message.chat.id, "Введите корректное количество виртов (от 50 тыс до 45 млн).")

# Обработка кнопки Кейсы
@bot.message_handler(lambda message: message.text == 'Кейсы')
def send_cases(message):
    markup = types.InlineKeyboardMarkup()
    for case_name, case_price in cases.items():
        markup.add(types.InlineKeyboardButton(text=f"{case_name} - {case_price} руб.", callback_data=f"case_{case_name}"))
    bot.send_message(message.chat.id, "Доступные кейсы:", reply_markup=markup)

# Обработка выбора кейса
@bot.callback_query_handler(func=lambda call: call.data.startswith('case_'))
def case_details(call):
    case_name = call.data.split('case_')[1]
    case_price = cases[case_name]
    text = f"Кейс: {case_name}\nЦена: {case_price} руб."
    payment_methods = types.InlineKeyboardMarkup()
    payment_methods.add(types.InlineKeyboardButton(text="Телеграм кошелек", url="https://t.me/wallet/"))
    payment_methods.add(types.InlineKeyboardButton(text="Kaspi банк", callback_data="kaspi_payment"))
    payment_methods.add(types.InlineKeyboardButton(text="СБП", callback_data="sbp_payment"))
    bot.send_message(call.message.chat.id, text)
    bot.send_message(call.message.chat.id, "Выберите метод оплаты:", reply_markup=payment_methods)

# Обработка оплаты Kaspi
@bot.callback_query_handler(func=lambda call: call.data == 'kaspi_payment')
def kaspi_payment(call):
    bot.send_message(call.message.chat.id, "📩 Отправьте деньги по реквизитам на Kaspi Gold:\n☎️ Номер: 4400 4302 6934 6638\n👨‍💻 Имя - Данил Г.\n💬 Комментарий: НЕ ПИСАТЬ!!!")

# Обработка оплаты СБП
@bot.callback_query_handler(func=lambda call: call.data == 'sbp_payment')
def sbp_payment(call):
    bot.send_message(call.message.chat.id, "Оплатить можно на карту РОССИИ: 2200701089399395 Аким.\nПосле оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров.")

bot.polling()
