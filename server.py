import socket
import sqlite3

HOST = '127.0.0.1'
PORT = 5000

def check_activation_key(login, activation_key):
    # проверяем логин и ключ активации в базе данных
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE login=? AND activation_key=?", (login, activation_key))
    result = cur.fetchone()
    con.close()
    return bool(result)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[*] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print('Успешное соединение с адресом', addr)

            while True:
                data = conn.recv(1024)
                if not data:
                    break

                login, activation_key = data.decode().rstrip().split('\n')
                print(f"Полученные логин: {login}, ключ активации: {activation_key}")

                if check_activation_key(login, activation_key):
                    success_message = f'Аутентификация прошла успешно'
                    conn.sendall(success_message.encode('utf-8'))
                else:
                    failure_message = f'Неправильный логин или ключ активации'
                    conn.sendall(failure_message.encode('utf-8'))

            print(f"[-] Соединение закрыто с адресом {addr}")
