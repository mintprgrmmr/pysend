import socket
import errno

HOST: str = "127.0.0.1"
PORT: int = 1234
SIZE: int = 1024

SAVE_DIR: str = "test/data/saved"
REQUEST_NAME: str = "source.bin"
DESTINATION_NAME: str = "sendfile.txt"

def run_client() -> None:
    """
    Простой TCP-клиент: подключается к серверу, запрашивает REQUEST_NAME
    и сохраняет его как DEST_NAME в SAVE_DIR.
    """
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        clientsocket.connect((HOST, PORT))
        print(f"[CLIENT][CONNECTING]Установлено соединение с {HOST}:{PORT}.")

        print(f"[CLIENT][REQUEST] Запрос файла: {REQUEST_NAME}")
        clientsocket.send((REQUEST_NAME + "\n").encode())

        destinationpath = SAVE_DIR + "/" + DESTINATION_NAME

        file = open(destinationpath, "wb")
        print("[CLIENT][OPEN]Файл открыт для записи.\n[CLIENT][RECV] Прием содержимого...")
        while True:
            chunk: bytes = clientsocket.recv(SIZE)
            if not chunk:
                break
            file.write(chunk)
        file.close()
        print(f"[CLIENT][FINISHED] Прием завершен. Файл сохранен как {destinationpath}")

        clientsocket.close()

    except ConnectionRefusedError as er:
        if er.errno == errno.ECONNREFUSED:
            print("[CLIENT][ConnectionRefusedError]В подключении отказано: сервер не слушает порт. Клиент завершил работу.")
            exit(1)
        else:
            print("[CLIENT][ConnectionRefusedError]Ошибка подключения:", er)
    except FileNotFoundError:
        print(f"[CLIENT][FileNotFoundError] Не найден файл {destinationpath}. Проверь путь/имя.")
    except OSError as er:
        if er.errno == errno.EISCONN:
            print(f"[CLIENT][OSError]Сокет уже подключен: {er}. Клиент завершил работу.")
            exit(1)
        else:
            print(f"[CLIENT][OSError] Ошибка №{er.errno}: {er.strerror}")
    except Exception as er:
        print(f"[CLIENT][ERROR]Неожиданная ошибка при подключении к серверу: {er}")

def main() -> None:
    """
    Точка входа: запускает клиента.
    """
    run_client()

if __name__ == "__main__":
    main()