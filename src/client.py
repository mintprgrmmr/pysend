import socket

HOST: str = "127.0.0.1"
PORT: int = 1235
SIZE: int = 1024

SAVE_DIR: str = "test/data/saved"
REQUEST_NAME: str = "source.bin"
DESTINATION_NAME: str = "sendfile.txt"
STOP_MARK: bytes = b"__STOP__"

def run_client() -> None:
    """
    Простой UDP-клиент: отправляет имя файла серверу, 
    принимает содержимое файла до STOP_MARK и сохраняет его в SAVE_DIR/DESTINATION_NAME.
    """
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        clientsocket.connect((HOST, PORT))
        print(f"[CLIENT][CONNECTING]Клиент установил соединение с {HOST}:{PORT}.")

        print(f"[CLIENT][REQUEST] Запрос файла: {REQUEST_NAME}")
        clientsocket.send(REQUEST_NAME.encode())
        
        destinationpath = SAVE_DIR + "/" + DESTINATION_NAME

        try:
            file = open(destinationpath, "wb")
            print("[CLIENT][OPEN]Файл открыт для записи.")
            print("[CLIENT][RECV]Прием данных...")
            
            while True:
                data, _ = clientsocket.recvfrom(SIZE)
                if data == STOP_MARK:   
                    break
                file.write(data)
            file.close()
            print(f"[CLIENT][SENDING] Прием завершен. Файл сохранен как {destinationpath}.")
        except FileNotFoundError:
            print(f"[CLIENT][FileNotFoundError] Папка для сохранения не найдена: {destinationpath}")
        except Exception as er:
            print(f"[CLIENT][ERROR]Ошибка записи: {er}")

        clientsocket.close()

    except OSError as er:
        print(f"[OSError] Ошибка №{er.errno}: {er.strerror}")
    except Exception as er:
        print(f"[CLIENT][ERROR]Неожиданная ошибка: {er}")

def main() -> None:
    """
    Точка входа: запускает клиента.
    """
    run_client()

if __name__ == "__main__":
    main()