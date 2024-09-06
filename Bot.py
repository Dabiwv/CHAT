from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Токен вашего бота
TOKEN = '6692785864:AAEqASjDj-9JcmIZKGOjCSgvXWXDv7E7KaY'

# Данные для аккаунтов, виртов и кейсов
accounts = {
    6: {'price': 500, 'description': "Аккаунт 6 lvl, дом отсутствует, авто: Zhiguli"},
    10: {'price': 1500, 'description': "Аккаунт 10 lvl, есть квартира, авто: Toyota"},
    15: {'price': 3000, 'description': "Аккаунт 15 lvl, есть дом, авто: BMW"},
    23: {'price': 5000, 'description': "Аккаунт 23 lvl, есть вилла, авто: Mercedes"}
}

cases = {
    'Бомжа': 140,
    'Ежедневный': 300,
    'Стандартный': 400,
    'Особый': 500,
    'Кейс ха Блек коины': 700
}

# Вспомогательные функции
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Добро пожаловать!\nВыберите категорию:\n'
        '/accounts - Аккаунты\n'
        '/virts - Вирты\n'
        '/cases - Кейсы'
    )

def accounts(update: Update, context: CallbackContext):
    response = 'Выберите аккаунт:\n'
    for lvl, details in accounts.items():
        response += f"Уровень {lvl}: {details['price']} руб.\n"
    response += 'Введите номер уровня для получения описания.\n'
    update.message.reply_text(response)

def virts(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Здравствуйте, введите число виртов, мин 50 тыс, макс 45 млн.'
    )
    return 'waiting_virts'

def cases(update: Update, context: CallbackContext):
    response = 'Выберите кейс:\n'
    for name, price in cases.items():
        response += f"{name}: {price} руб.\n"
    response += 'Введите название кейса для получения информации.'
    update.message.reply_text(response)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if text.isdigit():
        handle_virts(update, text)
    else:
        handle_case_or_account(update, text)

def handle_virts(update: Update, amount_str: str):
    try:
        amount = int(amount_str)
        if 50000 <= amount <= 45000000:
            # Здесь нужно добавить расчет цены в рублях
            price = calculate_virts_price(amount)
            update.message.reply_text(f"Вирты:\nКоличество: {amount}\nЦена: {price} руб.")
            show_payment_instructions(update.message)
        else:
            update.message.reply_text('Число виртов должно быть в пределах от 50 тыс до 45 млн.')
    except ValueError:
        update.message.reply_text('Введите корректное число виртов.')

def calculate_virts_price(amount: int) -> int:
    # Примерная цена, можно изменить по вашему усмотрению
    return amount // 1000

def handle_case_or_account(update: Update, text: str):
    if text.startswith('Уровень'):
        lvl = int(text.split(' ')[1])
        if lvl in accounts:
            account = accounts[lvl]
            update.message.reply_text(f"Уровень {lvl}:\nОписание: {account['description']}\nЦена: {account['price']} руб.")
            show_payment_instructions(update.message)
        else:
            update.message.reply_text('Такого уровня нет.')
    elif text in cases:
        price = cases[text]
        update.message.reply_text(f"{text}:\nЦена: {price} руб.")
        show_payment_instructions(update.message)
    else:
        update.message.reply_text('Неизвестная команда или категория.')

def show_payment_instructions(message):
    instructions = (
        'Выберите метод оплаты:\n'
        '1. Телеграм кошелек: UQC8Y2ZLGUJSmAasHTw_VNvO5jQ4w4OeJC_DQBO-wnqUItAL\n'
        '2. Каспи банк:\n'
        '📩 Отправьте деньги по реквизитам на Kaspi Gold 🔥:\n'
        '☎️ Номер: 4400 4302 6934 6638\n'
        '👨‍💻 Имя - Данил Г.\n'
        '💬 Комментарий: НЕ ПИСАТЬ!!!\n'
        '3. СБП:\n'
        'Оплатить можно на карту РОССИИ: 2200701089399395 Аким.\n'
        'После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров'
    )
    message.reply_text(instructions)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('accounts', accounts))
    dp.add_handler(CommandHandler('virts', virts))
    dp.add_handler(CommandHandler('cases', cases))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
