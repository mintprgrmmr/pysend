import socket
import errno

HOST: str = "127.0.0.1"
PORT: int = 1234
SIZE: int = 1024

SOURCE_DIR: str = "test/data/source"
SOURCE_NAME: str = "source.bin"

def run_server() -> None:
    """
    Простой TCP-сервер: ждет запрос имени файла от клиента, 
    читает файл локально и передаёт его содержимое клиенту.
    """
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("[SERVER][BOOT]Сокет успешно создан.")

    try:
        serversocket.bind((HOST, PORT))
        print(f"[SERVER][STARTING]Cервер запущен на {HOST}:{PORT}.")

        serversocket.listen(5)
        print("[SERVER][LISTENING]Ожидание подключений...")

    except OSError as er:
        if er.errno == errno.EADDRINUSE:
            print(f"[SERVER][OSError]Порт {PORT} уже занят. Завершение работы\nСервер завершил работу.")
            exit(1)
    except Exception as er:
        print(f"[SERVER][ERROR]Неожиданная ошибка при запуске сервера: {er}")
        exit(1)

    while True:
        clientsocket, clientaddr = serversocket.accept()
        print("[SERVER][CLIENT]Подключился клиент:", clientaddr)

        filenamebytes: bytes = clientsocket.recv(SIZE)
        if not filenamebytes: 
            print("[SERVER][CLIENT]Соединение разорвано.")
            clientsocket.close()
            continue

        requestedname: str = filenamebytes.decode().strip()
        print(f"[SERVER][REQUEST]Запрошен файл: {requestedname}. Попытка отправки содержимого файла...")
        if requestedname != SOURCE_NAME:
            print("[SERVER][ERROR]Запрошен неизвестный файл. Соединение будет закрыто.")
            clientsocket.close()
            print("[SERVER][CLOSE]Соединение закрыто.")
            continue

        sourcepath = SOURCE_DIR + "/" + SOURCE_NAME
        try:
            file = open(sourcepath, "rb")
            print("[SERVER][SENDING]Передача данных...")
            while True:
                chunk: bytes = file.read(SIZE)
                if not chunk:
                    break
                clientsocket.sendall(chunk)
            file.close()
            print("[SERVER][FINISHED]Передача данных завершена.")
        except FileNotFoundError:
            print(f"[SERVER][ERROR]Файл не найден: {sourcepath}")
        except Exception as er:
            print(f"[SERVER][ERROR]Неожиданная ошибка при получении файла: {er}")

        clientsocket.close()
        print ("[SERVER][CLOSE]Соединение закрыто.")

def main():
    """
    Точка входа: запускает сервер.
    """
    run_server()

if __name__ == "__main__":
    main()