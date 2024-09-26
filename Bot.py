import smtplib
from email.mime.text import MIMEText
from getpass import getpass

def send_email(to_email, username_or_id, violation_link, num_requests):
    # Настройки почты
    from_email = input("Введите ваш адрес электронной почты: ")
    password = getpass("Введите пароль от почты: ")

    # Текст жалобы
    complaint_text = f"""Дорогая поддержка телеграм, данный пользователь оскорбляет мою религию и мои интересы: {violation_link} (юзернейм/ID: {username_or_id})."""

    # Создаем сообщение
    msg = MIMEText(complaint_text)
    msg['Subject'] = 'Жалоба на пользователя'
    msg['From'] = from_email
    msg['To'] = to_email

    # Список адресов для отправки
    email_addresses = [
        "abuse@telegram.org",
        "sticker@telegram.org",
        "support@telegram.org",
        "stopCA@telegram.org",
        "dmca@telegram.org"
    ]

    # Отправка сообщения несколько раз
    for _ in range(num_requests):
        for email in email_addresses:
            try:
                # Подключаемся к SMTP серверу
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()  # Защищенное соединение
                    server.login(from_email, password)  # Входим в почту
                    server.sendmail(from_email, email, msg.as_string())  # Отправка сообщения
                    print(f'Жалоба отправлена на {email}')
            except Exception as e:
                print(f'Ошибка при отправке на {email}: {e}')

if __name__ == "__main__":
    username_or_id = input("Введите юзернейм или ID пользователя: ")
    violation_link = input("Введите ссылку на нарушение: ")
    num_requests = int(input("Сколько запросов отправить? "))
    
    send_email("example@example.com", username_or_id, violation_link, num_requests)
