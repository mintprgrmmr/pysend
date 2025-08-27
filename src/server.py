import socket
import errno

HOST = "127.0.0.1"
PORT = 1234

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("[+] Сокет успешно создан.")

try:
    serversocket.bind((HOST, PORT))
    print(f"[+] Cервер запущен на {HOST}:{PORT}.")

    serversocket.listen(5)
    print("[+] Ожидание подключений...")

except OSError as er:
    if er.errno == errno.EADDRINUSE:
        print(f"[-] Порт {PORT} уже занят. Завершение работы\nСервер завершил работу.")
        exit(1)
except Exception as er:
    print(f"[-] Неожиданная ошибка при запуске сервера: {er}")

while True:
    clientsocket, clientaddr = serversocket.accept()
    print("[+] Подключился клиент:", clientaddr)

    data = clientsocket.recv (1024)
    if not data:
        print("[-] Клиент разорвал соединение.")
        break
    message = data.decode()
    print(f"[+] Клиент отправил: {message}")
    message = "-> Hello client!" \
    
    clientsocket.send (message.encode())

    clientsocket.close()