import socket
import threading

host = '127.0.0.1'
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

rooms = [{} for i in range(50)]
nicknames = {}


def room(client, address):
    for i in range(len(rooms)):
        if not rooms[i]:
            rooms[i][address] = client
            return True
        elif len(rooms[i]) == 1:
            rooms[i][address] = client
            return True
        elif len(rooms[i]) == 2 and i == 49:
            return False


def broadcast(message, address, client):
    for i in range(len(rooms)):
        if (address in rooms[i]) and len(rooms[i]) == 2:
            for element in rooms[i]:
                print(element)
                rooms[i][element].send(message)
            return
        elif len(rooms[i]) != 2:
            client.send(message)
            return


def message_after_die(address, nickname):
    for i in range(len(rooms)):
        if (address in rooms[i]) and len(rooms[i]) == 2:
            for element in rooms[i]:
                if element != address:
                    print(element)
                    rooms[i][element].send('{} покинул чатчат'.format(nickname).encode('utf-8'),)
            return


def handle(client, address):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, address, client)
        except:
            nickname = nicknames[address]
            message_after_die(address, nickname)
            for i in range(len(rooms)):
                if address in rooms[i]:
                    del rooms[i][address]
            print(rooms)
            client.close()
            del nicknames[address]
            break


def take():  # Подключение нескольких клиентов
    while True:
        client, address = server.accept()
        print("Соединён с {}".format(str(address)))
        client.send('NICKNAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        # nicknames.append(nickname)
        # print(str(server))
        if not room(client, address):
            print("нет мест(")
        nicknames[address] = nickname
        print(rooms)
        # print(client)
        print("Имя пользователя {}".format(nickname))
        broadcast("{} присоединился к чату".format(nickname).encode('utf-8'), address, client)
        thread = threading.Thread(target=handle, args=(client, address, ))
        thread.start()


take()
