import socket
import errno

HOST: str = "127.0.0.1"
PORT: int = 1234
SIZE: int = 1024
SOURCE_DIR: str = "test/data/source"
SOURCE_NAME: str = "source.bin"
SEND_NAME: str = "sendfile.txt"

def run_client() -> None:
    """
    Простой TCP-клиент: подключается к серверу, отправляет имя файла
    и его содержимое в байтах, затем ждёт подтверждение и закрывает соединение.
    """
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        clientsocket.connect((HOST, PORT))
        print(f"[CONNECTING]Клиент установил соединение с {HOST}:{PORT}.")

        print(f"[REQUESTING] Имя файла для отправки: {SEND_NAME}")
        clientsocket.send((SEND_NAME + "\n").encode())

        file = open(SOURCE_DIR + "/" + SOURCE_NAME, "rb")
        print("[OPEN]Файл открыт для чтения в бинарном режиме.\n[SENDING] Отправка содержимого файла...")
        while True:
            chunk: bytes = file.read(SIZE)
            if not chunk:
                break
            clientsocket.sendall(chunk)
        file.close()

        clientsocket.shutdown(socket.SHUT_WR)
        print("[SENDING] Отправка завершена.")

        message: str = clientsocket.recv(SIZE).decode()
        print(f"[SERVER] Ответ:{message}")

        clientsocket.close()

    except ConnectionRefusedError as er:
        if er.errno == errno.ECONNREFUSED:
            print("[ConnectionRefusedError]В подключении отказано: сервер не слушает порт. Клиент завершил работу.")
            exit(1)
        else:
            print("[ConnectionRefusedError]Ошибка подключения:", er)
    except FileNotFoundError:
        print(f"[FileNotFoundError] Не найден файл {SOURCE_NAME}. Проверь путь/имя.")
    except OSError as er:
        if er.errno == errno.EISCONN:
            print(f"[OSError]Сокет уже подключен: {er}. Клиент завершил работу.")
            exit(1)
        else:
            print(f"[OSError] Ошибка №{er.errno}: {er.strerror}")
    except Exception as er:
        print(f"[ERROR]Неожиданная ошибка при подключении к серверу: {er}")

def main() -> None:
    """
    Точка входа: запускает клиента.
    """
    run_client()

if __name__ == "__main__":
    main()