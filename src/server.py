import socket
import errno

HOST: str = "127.0.0.1"
PORT: int = 1235
SIZE: int = 1024
SAVE_DIR: str = "test/data/saved"
STOP_MARK: bytes = b"__STOP__"

def run_server() -> None:
    """
    Простой UDP-сервер: принимает имя файла и содержимое,
    сохраняет его в SAVE_DIR и отправляет подтверждение клиенту.
    """
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.bind((HOST, PORT))
    print ("[BOOT]Сокет успешно создан, сервер слушает",(HOST, PORT))

    while True:
            filenamepacket, clientaddr = serversocket.recvfrom(SIZE)
            print("[CLIENT]Подключился клиент:", clientaddr)
            if not filenamepacket: 
                print("[CLIENT]Пустое имя файла --> Пропущено.")
                continue

            filename: str = filenamepacket.decode().strip()
            print("[RECV]Получены данные о файле.")
            print(f"[CLIENT]Имя файла: {filename}.\n[RECV] Приём содержимого файла...")
            
            filepath = SAVE_DIR + "/" + filename

            try:
                fileout = open(filepath, "wb")
                print("[OPEN]Файл открыт для перезаписи в бинарном режиме.")
            
                while True:
                    chunk, from_addr = serversocket.recvfrom(SIZE)
                    if from_addr != clientaddr:
                        print(f"[SKIP] Получен пакет от чужого клиента {from_addr}, жду данные от {clientaddr}.")
                        continue
                    if chunk == STOP_MARK:   
                        break
                    fileout.write(chunk)
            
                fileout.close()
                print("[FINISHED] Файл успешно сохранён.")

                serversocket.sendto(b"THANKS FOR FILE BRO!!!", clientaddr)
                print("[ACK] Подтверждение отправлено клиенту.")

            except FileNotFoundError:
                print(f"[ERROR] Папка {SAVE_DIR} не существует. Создайте её перед запуском.")
            except Exception as er:
                print(f"[ERROR]Неожиданная ошибка при получении файла: {er}")

def main():
    """
    Точка входа: запускает сервер.
    """
    run_server()

if __name__ == "__main__":
    main()
