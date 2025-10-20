import asyncio
import websockets
import pika
import threading

# Função para consumir mensagens do RabbitMQ (respostas para o cliente)
def consume_responses(websocket):

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='server_to_client')
    
    def callback(ch, method, properties, body):

        response = body.decode('utf-8')
        print(f"Enviando resposta ao cliente: {response}")
        asyncio.run(websocket.send(response))  

        if response == "tt":
            connection.close()
    

    channel.basic_consume(queue='server_to_client', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


# Handler para WebSocket
async def chat_handler(websocket, path):
    print("Cliente conectado via WebSocket")
    
    # Inicia thread para consumir respostas do RabbitMQ
    threading.Thread(target=consume_responses, args=(websocket,)).start()
    
    try:
        async for message in websocket:
            print(f"Mensagem recebida via WebSocket: {message}")
            if message == "tt":
                print("Conversa encerrada")
                break
            
            # Publica mensagem na fila RabbitMQ para processamento
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='client_to_server')
            channel.basic_publish(exchange='', routing_key='client_to_server', body=message)
            connection.close()
            
            # Simula processamento: publica resposta na fila (pode ser feito por outro worker)
            response = input("Sua resposta (processada via RabbitMQ): ")
            connection_resp = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel_resp = connection_resp.channel()
            channel_resp.queue_declare(queue='server_to_client')
            channel_resp.basic_publish(exchange='', routing_key='server_to_client', body=response)
            connection_resp.close()
            
    except websockets.exceptions.ConnectionClosed:
        print("Conexão WebSocket fechada")

async def main():
    server = await websockets.serve(chat_handler, "localhost", 8888)
    print("Servidor integrado (WebSocket + RabbitMQ) rodando em ws://localhost:8888")
    await server.wait_closed()

asyncio.run(main())