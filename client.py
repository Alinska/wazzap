import asyncio
import websockets
import socket
import datetime

async def receive_messages(websocket):
    async for message in websocket:
        ###
        #
        print(message) # we add timestamp in client_messages function in server.py

async def send_messages(websocket):
    try:
        while True:
            message = await asyncio.to_thread(input, "> ") # waiting for user input 
                                                       #now = datetime.datetime.now().strftime("%d/%m%Y %H:%M")
                                                       #message = await asyncio.to_thread(input, f"{now} - {socket.gethostname()}: ")
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosedError:
        print("Server is unreachable")

async def connect_to_server():
    uri = "ws://127.0.0.1:8080"
    async with websockets.connect(uri) as websocket:
        print(f"Connected to {uri}") #quality of life
        await asyncio.gather(
            receive_messages(websocket),
            send_messages(websocket)
        )

asyncio.run(connect_to_server())
