import socket



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8888))


finished = False
print('digite tt para terminar a conversa')


while not finished:

    client.send(input('Mensagem Cliente: ').encode('utf-8'))
    message = client.recv(1024).decode('utf-8')


    if message == 'tt':
        finished = True
    else:
        print(message)
        


client.close()