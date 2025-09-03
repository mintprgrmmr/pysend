import socket

HOST: str = "127.0.0.1"
PORT: int = 1235
SIZE: int = 1024

SOURCE_DIR: str = "test/data/source"
SOURCE_NAME: str = "source.bin"
STOP_MARK: bytes = b"__STOP__"

def run_server() -> None:
    """
    Простой UDP-сервер: ждёт имя файла от клиента, читает локальный файл
    и отправляет его содержимое клиенту частями. В конце шлёт STOP_MARK.
    """
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.bind((HOST, PORT))
    print ("[SERVER][BOOT]Сокет успешно создан, сервер слушает",(HOST, PORT))

    while True:
            filenamepacket, clientaddr = serversocket.recvfrom(SIZE)
            print("[SERVER][CLIENT]Подключился клиент:", clientaddr)
            if not filenamepacket: 
                print("[SERVER][CLIENT]Пустое имя файла --> пропуск.")
                continue

            requestedname: str = filenamepacket.decode().strip()
            print(f"[SERVER][REQUEST]Запрошен файл: {requestedname}.\n[SERVER][SENDING]Попытка отправки содержимого файла...")

            if requestedname != SOURCE_NAME:
                print("[SERVER][ERROR]Запрошен неизвестный файл. Соединение закрыто.")
                continue
            
            sourcepath = SOURCE_DIR + "/" + SOURCE_NAME
            try:
                file = open(sourcepath, "rb")
                print("[SERVER][SENDING]Передача данных...")
                while True:
                    chunk: bytes = file.read(SIZE)
                    if not chunk:
                        break
                    serversocket.sendto(chunk, clientaddr)
                serversocket.sendto(STOP_MARK, clientaddr)
                print("[SERVER][FINISHED] Передача файла завершена.")

            except FileNotFoundError:
                print(f"[SERVER][ERROR] Файл не найден: {sourcepath}.")
            except Exception as er:
                print(f"[SERVER][ERROR]Неожиданная ошибка при получении файла: {er}")

def main():
    """
    Точка входа: запускает сервер.
    """
    run_server()

if __name__ == "__main__":
    main()
