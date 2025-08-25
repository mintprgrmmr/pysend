import socket

HOST = "127.0.0.1"
PORT = 1234

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Сокет успешно создан")

try:
    serversocket.bind((HOST, PORT))
    print(f"Сервер запущен на {HOST}:{PORT}")
    serversocket.listen(5)
    print("Ожидание подключений...")
except OSError as er:
    print("Системная ошибка при запуске сервера:", er)
except Exception as er:
    print(f"Неожиданная ошибка при запуске сервера: {er}")

try:
    conn, addr = serversocket.accept()
    print(addr)
except Exception as er:
    print(f"Ошибка при приёме подключения: {er}")