import socket
import errno

HOST = "127.0.0.1"
PORT = 1234
SIZE = 1024

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientsocket.connect((HOST, PORT))
    print(f"[CONNECTING]Клиент установил соединение с {HOST}:{PORT}.")

    filename = "sendfile.txt"
    print(f"[REQUESTING] Имя файла для отправки: {filename}")
    clientsocket.send((filename + "\n").encode())

    file = open("data/sendfile.txt", "rb")
    print("[OPEN]Файл открыт для чтения в бинарном режиме.\n[SENDING] Отправка содержимого файла...")
    while True:
        chunk = file.read(SIZE)
        if not chunk:
            break
        clientsocket.sendall(chunk)
    file.close()

    clientsocket.shutdown(socket.SHUT_WR)
    print("[SENDING] Отправка завершена.")

    message = clientsocket.recv(SIZE).decode()
    print(f"[SERVER] Ответ:{message}")

    clientsocket.close()

except ConnectionRefusedError as er:
    if er.errno == errno.ECONNREFUSED:
        print("[ConnectionRefusedError]В подключении отказано: сервер не слушает порт. Клиент завершил работу.")
        exit(1)
    else:
        print("[ConnectionRefusedError]Ошибка подключения:", er)
except OSError as er:
    if er.errno == errno.EISCONN:
        print(f"[OSError]Сокет уже подключен: {er}. Клиент завершил работу.")
        exit(1)
    else:
        print(f"[OSError] Ошибка №{er.errno}: {er.strerror}")
except FileNotFoundError:
    print(f"[FileNotFoundError] Не найден файл {filename}. Проверь путь/имя.")
except Exception as er:
    print(f"[ERROR]Неожиданная ошибка при подключении к серверу: {er}")