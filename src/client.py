import socket
import errno

HOST: str = "127.0.0.1"
PORT: int = 1234
SIZE: int = 1024
SOURCE_DIR: str = "test/data/source"
SOURCE_NAME: str = "source.bin"
SEND_NAME: str = "sendfile.txt"