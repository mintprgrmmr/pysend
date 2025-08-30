import socket
import errno

HOST: str = "127.0.0.1"
PORT: int = 1235
SIZE: int = 1024
SOURCE_DIR: str = "test/data/source"
SOURCE_NAME: str = "source.bin"
SEND_NAME: str = "sendfile.txt"

def run_client() -> None:
    """
    Простой UDP-клиент: подключается к серверу, отправляет имя файла
    и его содержимое в байтах, затем ждёт подтверждение и закрывает соединение.
    """
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



def main() -> None:
    """
    Точка входа: запускает клиента.
    """
    run_client()

if __name__ == "__main__":
    main()