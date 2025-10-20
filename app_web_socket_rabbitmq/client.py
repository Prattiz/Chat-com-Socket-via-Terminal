import asyncio
import websockets

async def chat():
    uri = "ws://localhost:8888"
    async with websockets.connect(uri) as websocket:
        print("Conectado ao servidor integrado. Digite 'tt' para sair.")
        while True:
            message = input("Sua mensagem: ")
            await websocket.send(message)
            if message == "tt":
                break
            response = await websocket.recv()
            print(f"Servidor: {response}")

asyncio.run(chat())