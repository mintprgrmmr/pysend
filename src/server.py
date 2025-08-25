import socket

HOST = socket.gethostname()
PORT = 1234

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Сокет успешно создан")

try:
    serversocket.bind((HOST, PORT))
    print(f"Сервер запущен на {HOST}:{PORT}")
    serversocket.listen(5)
    print("Ожидание подключений...")
except Exception as er:
    print(f"Ошибка при запуске сервера: {er}")

try:
    conn, addr = serversocket.accept()
    print(addr)
except Exception as er:
    print(f"Ошибка при приёме подключения: {er}")

try:
    serversocket.recv()
    print(f"Файл получен")
except Exception as er:
    print(f"Ошибка при приёме подключения: {er}")