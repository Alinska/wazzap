# import asyncio
# import websockets
# import datetime

# async def receive_messages(websocket):
#     async for message in websocket:
#         now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
#         print(f"{now} - Server: {message}")

# async def send_messages(websocket):
#     try:
#         while True:
#             now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
#             message = await asyncio.to_thread(input, f"\n")
#             await websocket.send(f"{message}")
#     except websockets.exceptions.ConnectionClosedError:
#         print("Server is unreachable")

# async def connect_to_server():
#     uri = "ws://127.0.0.1:8080"
    
#     async with websockets.connect(uri) as websocket:
#         print("Connection to Wazzap server successful!\nType here to communicate with the server...\n")
#         await asyncio.gather(
#             receive_messages(websocket),
#             send_messages(websocket)
#         )

# asyncio.run(connect_to_server())

import asyncio
import websockets


async def listen(websocket):

    #Continuously listen for incoming messages from the WebSocket server
    #and print them to the console.
    try:
        async for message in websocket:
            print(message)
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")


async def send_messages(websocket):

    #Continuously read input from the user and send it to the WebSocket server.
    #Uses asyncio.to_thread to run blocking input() call in a thread pool
    #so it doesn't block the event loop.

    try:
        while True:
            # Read user input asynchronously to avoid blocking the event loop
            message = await asyncio.to_thread(input, "> ")
            if not message:
                continue
            # Send the message to the server
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")


async def main(host="localhost", port=8080):
    print("Connection to server initiated")

    #Main function that establishes a WebSocket connection and runs
    #both listen and send_messages concurrently.


    # Erstellt die WebSocket-URI (Uniform Resource Identifier) für die Verbindung
    # Format: "ws://hostname:port" (z.B. "ws://localhost:8080")

    uri = f"ws://{host}:{port}"
    async with websockets.connect(uri) as websocket:
        # Run both listen and send_messages concurrently
        await asyncio.gather(listen(websocket), send_messages(websocket))
        

if __name__ == "__main__":
    asyncio.run(main())