import socket
import threading

# Настройка сервера
host = "0.0.0.0"  # Сервер принимает соединения на всех IP
port = 12345

# Создание сокета
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Список подключенных клиентов
clients = []
usernames = []

# Обработка сообщений от клиентов
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            broadcast(message, client)
        except:
            # Удаление клиента в случае ошибки
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f"{username} покинул чат.".encode("utf-8"), None)
            usernames.remove(username)
            break

# Рассылка сообщения всем клиентам
def broadcast(message, sender_client):
    for client in clients:
        if client != sender_client:
            client.send(message.encode("utf-8"))

# Главная функция для приема клиентов
def receive_connections():
    print("Сервер запущен, ожидаем подключения клиентов...")
    while True:
        client, address = server.accept()
        print(f"Новое соединение: {str(address)}")

        client.send("USERNAME".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")
        usernames.append(username)
        clients.append(client)

        print(f"Имя пользователя: {username}")
        broadcast(f"{username} присоединился к чату!".encode("utf-8"), None)
        client.send("Соединение с чатом установлено!".encode("utf-8"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Запуск сервера
receive_connections()
