import socket
import errno

HOST = "127.0.0.1"
PORT = 1234
SIZE = 1024

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("[BOOT]Сокет успешно создан.")

try:
    serversocket.bind((HOST, PORT))
    print(f"[STARTING]Cервер запущен на {HOST}:{PORT}.")

    serversocket.listen(5)
    print("[LISTENING]Ожидание подключений...")

except OSError as er:
    if er.errno == errno.EADDRINUSE:
        print(f"[OSError]Порт {PORT} уже занят. Завершение работы\nСервер завершил работу.")
        exit(1)
except Exception as er:
    print(f"[ERROR]Неожиданная ошибка при запуске сервера: {er}")

while True:
    clientsocket, clientaddr = serversocket.accept()
    print("[CLIENT]Подключился клиент:", clientaddr)

    filenamebytes = clientsocket.recv(SIZE)
    print("[RECV]Получены данные о файле.")
    if not filenamebytes: 
        print("[CLIENT]Соединение разорвано.")
        clientsocket.close()
        continue

    filename = filenamebytes.decode().strip()
    print(f"[CLIENT]Имя файла: {filename}.\n[RECV] Приём содержимого файла...")

    fileout = open(filename, "wb")
    print("[OPEN]Файл открыт для перезаписи в бинарном режиме.")
    while True:
        chunk = clientsocket.recv(SIZE)
        if not chunk:
            break
        fileout.write(chunk)
    fileout.close()
    print("[FINISHED] Файл успешно сохранён.")     

    try:
        clientsocket.send(b"THANKS FOR FILE BRO!!!")
        print("[ACK] Подтверждение отправлено клиенту.")
    except Exception as er:
        print(f"[ERROR]Неожиданная ошибка при получении файла: {er}")

    clientsocket.close()