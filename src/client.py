import socket

HOST: str = "127.0.0.1"
PORT: int = 1235
SIZE: int = 1024
SOURCE_DIR: str = "test/data/source"
SOURCE_NAME: str = "source.bin"
SEND_NAME: str = "sendfile.txt"
STOP_MARK: bytes = b"__STOP__"

def run_client() -> None:
    """
    Простой UDP-клиент: подключается к серверу, отправляет имя файла
    и его содержимое в байтах, затем ждёт подтверждение и закрывает соединение.
    """
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        clientsocket.connect((HOST, PORT))
        print(f"[CONNECTING]Клиент установил соединение с {HOST}:{PORT}.")

        print(f"[REQUESTING] Имя файла для отправки: {SEND_NAME}")
        clientsocket.send(SEND_NAME.encode())

        file = open(SOURCE_DIR + "/" + SOURCE_NAME, "rb")
        print("[OPEN]Файл открыт для чтения в бинарном режиме.\n[SENDING] Отправка содержимого файла...")
        while True:
            chunk: bytes = file.read(SIZE)
            if not chunk:
                break
            clientsocket.send(chunk)
        file.close()

        clientsocket.send(STOP_MARK)
        print("[SENDING] Отправка завершена.")

        message: str = clientsocket.recv(SIZE).decode()
        print(f"[SERVER] Ответ:{message}")

        clientsocket.close()

    except FileNotFoundError:
            print(f"[FileNotFoundError] Не найден файл {SOURCE_NAME}. Проверь путь/имя.")
    except OSError as er:
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