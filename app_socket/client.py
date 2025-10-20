import socket



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8888))


terminado = False
print('digite tt para terminar a conversa')


while not terminado:

    client.send(input('Mensagem: ').encode('utf-8'))
    message = client.recv(1024).decode('utf-8')


    if message == 'tt':
        terminado = True
    else:
        print(message)
        


client.close()