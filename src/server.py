import socket
import errno

HOST: str = "127.0.0.1"
PORT: int = 1235
SIZE: int = 1024
SAVE_DIR: str = "test/data/saved"

def run_server() -> None:
    """
    Простой UDP-сервер: принимает имя файла и содержимое,
    сохраняет его в SAVE_DIR и отправляет подтверждение клиенту.
    """
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



def main():
    """
    Точка входа: запускает сервер.
    """
    run_server()

if __name__ == "__main__":
    main()