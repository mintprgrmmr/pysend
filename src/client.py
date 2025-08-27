import socket
import errno

HOST = "127.0.0.1"
PORT = 1234

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientsocket.connect((HOST, PORT))
    print(f"[+] Клиент установил соединение с {HOST}:{PORT}.")

    message = "Hello server!"
    clientsocket.send (message.encode())
    
    data = clientsocket.recv (1024)
    reply = data.decode()
    print("[+] Ответ сервера:", reply)

    clientsocket.close()

except ConnectionRefusedError as er:
    if er.errno == errno.ECONNREFUSED:
        print(f"[-] В подключении отказано: сервер не слушает порт. Клиент завершил работу.")
        exit(1)
    else:
        print("[-] Ошибка подключения:", er)
except Exception as er:
    print(f"[-] Неожиданная ошибка при подключении к серверу: {er}")