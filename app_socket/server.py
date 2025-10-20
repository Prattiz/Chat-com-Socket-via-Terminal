import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('localhost', 8888))

server.listen()

client, addr = server.accept()


terminado = False

while not terminado:
    
    message = client.recv(1024).decode('utf-8')

    if message == 'tt':
        terminado = True
    else:
        print(message)
        client.send(input('Mensagem Servidor: ').encode('utf-8'))

client.close()
server.close()
        