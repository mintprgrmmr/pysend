#!/usr/bin/env bash

echo "[TEST]Подготовка каталогов..."
mkdir -p test/data/source test/data/saved

SOURCE_PATH="test/data/source/source.bin"
DESTINATION_PATH="test/data/saved/sendfile.txt"  

echo "[TEST]Удаление старых файлов..."
rm -f "$SOURCE_PATH" "$DESTINATION_PATH"

echo "[TEST]Генерация файла (2MB случайных байт)..."
head -c 2000000 /dev/urandom > "$SOURCE_PATH"

echo "[TEST]Старт сервера..."
python3 src/server.py &
SERVER_PID=$!
sleep 1

echo "[TEST]Старт клиента..."
python3 src/client.py

echo "[TEST]Проверка результата..."
cmp "$SOURCE_PATH" "$DESTINATION_PATH" \
  && echo "[TEST]OK: файлы совпадают." \
  || echo "[TEST]FAIL: файлы различаются."

echo "[TEST]Остановка сервера..."
kill "$SERVER_PID" 2>/dev/null || true

read -p "[TEST]Готово. Нажмите Enter, чтобы закрыть."