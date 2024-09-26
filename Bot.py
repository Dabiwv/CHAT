import smtplib
from email.mime.text import MIMEText

# Функция для отправки жалобы
def send_complaint(user_identifier, num_requests):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    your_email = 'ваша_почта@gmail.com'
    your_password = 'ваш_пароль'  # Используйте пароль от вашей почты

    # Список почтовых адресов для отправки жалоб
    email_addresses = [
        'dmca@telegram.org',
        'abuse@telegram.org',
        'sticker@telegram.org',
        'support@telegram.org',
        'stopCA@telegram.org'
    ]

    subject = 'Жалоба на пользователя Telegram'
    body_template = f"""Дорогая поддержка Telegram,
    данный пользователь оскорбляет мою религию и мои интересы. Вот ссылка на нарушение: {user_identifier}.
    """

    # Отправка жалоб
    for _ in range(num_requests):
        for email in email_addresses:
            msg = MIMEText(body_template)
            msg['Subject'] = subject
            msg['From'] = your_email
            msg['To'] = email
            
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()  # Защищенное соединение
                server.login(your_email, your_password)
                server.sendmail(your_email, email, msg.as_string())
                print(f'Письмо отправлено на {email}')
            except Exception as e:
                print(f'Ошибка при отправке на {email}: {e}')
            finally:
                server.quit()

# Запрос у пользователя
user_identifier = input("Введите юзернейм, ID пользователя или ссылку на нарушение: ")
num_requests = int(input("Сколько запросов отправить? "))

# Вызов функции отправки жалоб
send_complaint(user_identifier, num_requests)
