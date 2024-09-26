import smtplib
from email.mime.text import MIMEText

# Ваша почта и пароль
your_email = 'makarkox52@gmail.com'
your_password = '09) 09) 09) 09) g'

# Функция для отправки жалобы
def send_complaint(username_or_id, report_link, num_requests):
    # Список адресов электронной почты
    email_addresses = [
        'abuse@telegram.org',
        'sticker@telegram.org',
        'support@telegram.org',
        'stopCA@telegram.org',
        'dmca@telegram.org'
    ]

    # Текст жалобы
    complaint_text = f"""Дорогая поддержка телеграм, данный пользователь оскорбляет мою религию и мои интересы: {report_link} (ID или юзернейм: {username_or_id})"""

    # Отправка жалобы на каждую почту
    for email in email_addresses:
        for _ in range(num_requests):
            try:
                # Создаем объект SMTP
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.starttls()  # Используем TLS
                    smtp.login(your_email, your_password)  # Логинимся

                    # Создаем MIMEText сообщение
                    msg = MIMEText(complaint_text)
                    msg['Subject'] = 'Жалоба на пользователя Telegram'
                    msg['From'] = your_email
                    msg['To'] = email

                    # Отправляем письмо
                    smtp.send_message(msg)
                    print(f'Жалоба успешно отправлена на {email}')
            except Exception as e:
                print(f'Ошибка при отправке на {email}: {e}')

# Запросы от пользователя
username_or_id = input("Введите юзернейм или ID пользователя: ")
report_link = input("Введите ссылку на нарушение: ")
num_requests = int(input("Сколько запросов отправить? "))

# Отправка жалобы
send_complaint(username_or_id, report_link, num_requests)
